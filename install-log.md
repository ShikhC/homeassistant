# Home Assistant Installation Log

**Target Hardware:** HP ProDesk 600 G3 DM
- CPU: Intel Core i5-6500T @ 2.5GHz
- RAM: 8GB DDR4
- Storage: 256GB SSD
- GPU: Intel HD Graphics 530
- OS (current): Windows 10 Pro (Refurbished)

**Installation Method:** Home Assistant OS (Generic x86-64) — full dedicated install
**Date Started:** 2026-06-11
**HAOS Version:** 17.3 (latest as of 2026-06-11)

---

## Step 1: Download Home Assistant OS Image

**Status:** Pending

**What to do:**
- Download the Generic x86-64 HAOS image from GitHub releases
- File: `haos_generic-x86-64-17.3.img.xz` (~300MB)

**Command (run on your Mac):**
```bash
cd ~/Downloads
curl -L -O https://github.com/home-assistant/operating-system/releases/download/17.3/haos_generic-x86-64-17.3.img.xz
```

**Verification:**
```bash
ls -lh ~/Downloads/haos_generic-x86-64-17.3.img.xz
```

---

## Step 2: Flash Image to USB Drive

**Status:** ✅ Complete (Rufus on Windows, GPT/UEFI)

**What you need:**
- USB flash drive (8GB or larger) — ALL DATA ON IT WILL BE ERASED

**Option A — Using Balena Etcher (GUI, easiest):**
1. Download Balena Etcher from https://etcher.balena.io/
2. Open Etcher
3. Click "Flash from file" → select `haos_generic-x86-64-17.3.img.xz`
4. Click "Select target" → choose your USB drive
5. Click "Flash!" and wait for completion

**Option B — Using command line (advanced):**
```bash
# Find your USB drive identifier
diskutil list

# Unmount the USB drive (replace diskN with your disk number, e.g., disk2)
diskutil unmountDisk /dev/diskN

# Flash the image (replace diskN — use rdiskN for faster writes)
xzcat ~/Downloads/haos_generic-x86-64-17.3.img.xz | sudo dd of=/dev/rdiskN bs=4M status=progress

# Eject when done
diskutil eject /dev/diskN
```

**⚠️ WARNING:** Double-check the disk number! Writing to the wrong disk will destroy data.

---

## Step 3: Configure HP ProDesk BIOS

**Status:** In Progress

**How to enter BIOS:**
- Power on the HP ProDesk → immediately press **F10** repeatedly

**Actual BIOS Layout (4 tabs):**
- Main
- Security (has: Administrator Tools, Security Configuration [TPM, Smart Cover, Intel SGX], Utilities [Hard Drive Utilities, System Management Command])
- Advanced (has: Boot Options)
- UEFI Drivers

**NOTE:** Secure Boot is NOT under Security tab on this firmware. It is under **Advanced → Boot Options** (or possibly under Security → Security Configuration, depending on firmware version).

**Settings to change:**

**A) Advanced → Boot Options:**
| Setting | Change to |
|---------|-----------|
| USB Boot | **Enabled** |
| UEFI Boot Order | Move **USB Hard Drive** to first position |
| Secure Boot | **Disabled** (if listed here) |
| Legacy Boot / CSM | **Disabled** (ensure UEFI-only mode) |
| Fast Boot | **Disabled** (optional, helps troubleshooting) |

**B) Security → Security Configuration:**
| Setting | Change to |
|---------|-----------|
| Secure Boot | **Disabled** (if listed here instead) |

**Save and exit:** Press **F10** to save changes

---

## Step 4: Boot from USB and Install

**Status:** ⚠️ Issue — HAOS ran from USB but did NOT auto-install to internal SSD

**What happened:**
- HAOS booted successfully from USB (Supervisor was running)
- After removing USB and rebooting: "Boot Device Not Found" error (HP 3F0)
- The generic x86-64 HAOS image runs from wherever it's flashed — it does NOT auto-install to another disk
- Internal SSD identified as: Samsung HPS0TEXH, NVMe, path `/dev/nvme0n1`

**Solution:** Use a Linux live USB to flash HAOS image directly to the NVMe SSD

---

## Step 4 (Revised): Flash HAOS Directly to Internal NVMe SSD

**Status:** In Progress

**Method:** Boot Linux live USB → use `dd` to write HAOS image to `/dev/nvme0n1`

**What you need:**
- USB 1: Linux live USB (Ubuntu/Debian) — for running the dd command
- USB 2: The HAOS USB we already flashed (for the image file), OR download the image from within Linux

**Preparation (on Windows, before starting):**

### A) Create a Linux Live USB with your second USB drive:
1. Download Ubuntu Desktop ISO: https://ubuntu.com/download/desktop (or use any Linux live ISO)
2. Flash it to the **second USB drive** using Rufus:
   - Device: second USB drive
   - Boot selection: the Ubuntu ISO
   - Partition scheme: GPT
   - Target: UEFI
3. Also copy `haos_generic-x86-64-17.3.img.xz` onto the HAOS USB (the first one) so we can access it from Linux
   - OR we'll download it directly from Linux if the HP ProDesk has ethernet/wifi

### B) Boot the Linux Live USB on the HP ProDesk:
1. Plug in the Linux USB (second drive)
2. Power on → press **F9** → select the Ubuntu USB
3. Choose "Try Ubuntu" (don't install)

### C) Flash HAOS to the internal NVMe SSD:
```bash
# Identify the internal NVMe drive (should be /dev/nvme0n1)
lsblk

# If you copied the image to the HAOS USB, mount it:
# Find the HAOS USB (probably /dev/sda1 or similar)
sudo mkdir /mnt/usb
sudo mount /dev/sda1 /mnt/usb
ls /mnt/usb/   # confirm you can see the .img.xz file

# OR download directly (if connected to internet):
wget https://github.com/home-assistant/operating-system/releases/download/17.3/haos_generic-x86-64-17.3.img.xz

# Flash HAOS to the NVMe SSD (THIS ERASES THE SSD):
xzcat /path/to/haos_generic-x86-64-17.3.img.xz | sudo dd of=/dev/nvme0n1 bs=4M status=progress

# Sync to ensure all data is written
sync
```

4. Shut down, remove the Linux USB
5. Power on — HP ProDesk should now boot HAOS from the internal NVMe SSD

---

## Step 5: Initial Setup (Onboarding)

**Status:** ✅ Complete — Home Assistant is live and accessible

**Wait:** After first boot from SSD, Home Assistant needs ~5-20 minutes to download and configure. Be patient.

**Access the web interface:**
```
http://homeassistant.local:8123
```

**If homeassistant.local doesn't work:**
- Check your router's DHCP client list for the IP address
- Or look at the console output on the HP ProDesk — it shows the IP
- Access via: `http://<IP_ADDRESS>:8123`

**Onboarding wizard steps:**
1. Create your admin account (name, username, password)
2. Set your home location (for weather, sun automations, time zone)
3. Choose which discovered devices/integrations to set up
4. Done! You're in the Home Assistant dashboard

---

## Step 6: Post-Install Recommendations

**Status:** In Progress

**HA Version Note:** This version renamed "Add-ons" to **"Apps"** in the Settings menu. Same functionality, new label.

**Menu mapping (old → new):**
- Add-ons → **Settings → Apps**
- General → **Settings → System → General**
- Backups → **Settings → System → Backups**

**Immediately after setup:**
```
Settings → System → Network
```
- Assign a **static IP** (or set a DHCP reservation on your router)
- This prevents the address from changing after a reboot

**Recommended first add-ons** (Settings → Add-ons → Add-on Store):
| Add-on | Purpose |
|--------|---------|
| File Editor | Edit config files from the browser |
| Terminal & SSH | SSH access for advanced config |
| Samba Share | Access config folder from your Mac via Finder |
| HACS | Community integrations and themes (install via browser) |

**Backup:**
- Settings → System → Backups → Create Backup
- Set up automatic backups before adding more integrations

---

## Step 7: Connect Smart Home Devices (Optional Next Steps)

**Status:** Pending

**If you have/plan Zigbee or Z-Wave devices:**
- Buy a USB coordinator (e.g., SONOFF Zigbee 3.0 Plus, Home Assistant SkyConnect)
- Plug into the HP ProDesk USB port
- Set up via: Settings → Devices & Services → Add Integration → ZHA or Zigbee2MQTT

**Common first integrations:**
- Mobile app (auto-discovered)
- Weather (auto-discovered based on location)
- Philips Hue / LIFX / other smart bulbs
- Google Home / Alexa (for voice control)

---

## Troubleshooting Log

### Issue 2: "Boot Device Not Found (3F0)" — ROOT CAUSE: 4Kn NVMe sector mismatch (2026-06-11)

**Error:** HP BIOS says "Boot Device Not Found" even after HAOS is written to NVMe via dd
**Root Cause:** Samsung NVMe SSD (MZVLB256HBHQ-000H7) uses **4Kn (4K native) sector size** — both logical AND physical = 4096 bytes. HAOS image is built assuming 512-byte sectors. After dd, the partition table offsets are misaligned and the kernel cannot parse any partitions.

**Evidence from `fdisk -l /dev/nvme0n1`:**
```
Sector size (logical/physical): 4096 bytes / 4096 bytes
GPT PMBR size mismatch (12582911 != 62514773)
Disklabel type: dos  ← kernel fell back to MBR because GPT is unreadable
```
- `lsblk` shows nvme0n1 with ZERO partitions even after `partprobe`
- 12582911 × 512 bytes = ~6GB = HAOS image size (data IS there, addressing is wrong)

**BIOS state:** Secure Boot disabled, Legacy Support disabled

**Solution options:**
1. ✅ Reformat NVMe to 512-byte LBA format using `nvme format` (if drive supports it)
2. Replace SSD with a 512e drive (~$30-40)
3. Run HAOS from USB permanently (not ideal)

**Fixes tried:**
- [x] dd to NVMe — data written but partitions unreadable due to 4Kn
- [x] partprobe — no effect, partition table structurally incompatible
- [x] Check NVMe supported LBA formats (`nvme id-ns`) — supports 512B (format 0) and 4096B (format 1)
- [x] Reformat drive to 512-byte sectors — ✅ SUCCESS with `nvme format --lbaf=0`
- [x] Re-flash HAOS after reformat — ✅ SUCCESS, Home Assistant is LIVE

---

### Issue 1: Balena Etcher "Something went wrong" error (2026-06-11)

**Error:** "Something went wrong. If it is a compressed image please check that the archive is not corrupted. The writer process ended unexpectedly."

**Environment:** Etcher on Windows, image downloaded via browser

**Root causes (in order of likelihood):**
1. Incomplete/corrupted download (browser downloads of large .xz files sometimes truncate)
2. Etcher doesn't have admin privileges (can't write raw to USB on Windows)
3. USB drive has bad sectors or is fake-capacity
4. Antivirus interfering with raw disk write

**Fixes tried:**
- [ ] Verify file size / re-download
- [ ] Run Etcher as Administrator
- [x] Try alternate tool (Rufus) — ✅ SUCCESS. Took ~10 min total (long "Please Wait" at 100% is normal cache flush). Status: READY.
- [ ] Try different USB drive

---

## Commands Run Log

| # | Date | Command | Result |
|---|------|---------|--------|
| 1 | 2026-06-11 | `curl -s https://api.github.com/repos/home-assistant/operating-system/releases/latest` | Confirmed latest version is 17.3 |
| 2 | 2026-06-11 | `sudo partprobe /dev/nvme0n1` | No effect — partitions still invisible |
| 3 | 2026-06-11 | `sudo fdisk -l /dev/nvme0n1` | Revealed 4096-byte sector size, GPT PMBR mismatch |
| 4 | 2026-06-11 | `sudo nvme id-ns /dev/nvme0n1 -H` | Drive supports LBA Format 0 (512B) and 1 (4096B, in use) |
| 5 | 2026-06-11 | `sudo nvme format /dev/nvme0n1 --lbaf=0` | PENDING — reformats drive to 512-byte sectors |

---
