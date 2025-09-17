---
date: 2025-09-16
lastmod: 2025-09-16
draft: false
slug: mounting-a-disk-image-with-multiple-partitions
title: Mounting a Disk Image with Multiple Partitions
description: Mounting a disk image that has multiple partitions in order to modify its contents.
---

This is how to modify a disk image. It'll use the Raspberry Pi OS disk image, for example, but these steps can be applied to any image.

You can't mount the image as a whole because it contains multiple partitions. However, you can mount each partition individually if you know the size and location of each partition. Examine the image by listing the partition tables using `fdisk -l`:

```
$ fdisk -l 2025-05-13-raspios-bookworm-arm64.img
Disk 2025-05-13-raspios-bookworm-arm64.img: 5.73 GiB, 6157238272 bytes, 12025856 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xd1876ee1

Device                                 Boot   Start      End  Sectors  Size Id Type
2025-05-13-raspios-bookworm-arm64.img1        16384  1064959  1048576  512M  c W95 FAT32 (LBA)
2025-05-13-raspios-bookworm-arm64.img2      1064960 12025855 10960896  5.2G 83 Linux
```

Looking at the output, there are two partitions, one for the bootloader and one for the root file system. The important thing to note is the starting sector of each partition by looking at the `Start` column -- the bootloader is located at sector 16384 and the root file system is located at sector 1064960. Looking at the "Sector size" information:

```
Sector size (logical/physical): 512 bytes / 512 bytes
```

we can find the offset of each partition from the beginning of the image and use that information to mount each partition.

Start by creating mount points for each partition:

```bash
$ mkdir img1 img2
```

Then mount each partition using the offset information from the previous steps by multiplying the starting sector by the sector size:

```bash
$ mount -v -o offset=$(( 512 * 16384 )) 2025-05-13-raspios-bookworm-arm64.img img1
$ mount -v -o offset=$(( 512 * 1064960 )) 2025-05-13-raspios-bookworm-arm64.img img2
```

{{<notice info>}}
If you get an error like "failed to setup loop device" check to make sure you permission to the `/dev/loop0` device. If you don't, run the `mount` commands with `sudo`.
{{</notice>}}

If you get an "overlapping loop device exists" error, you can try mounting only one partition at a time or specify the size as well as the offset. To find the size, use the number of sectors from the `Sectors` column multiplied by the sector size.

```bash
$ mount -v -o offset=$(( 512 * 16384 )),sizelimit=$(( 512 * 1048576 )) 2025-05-13-raspios-bookworm-arm64.img img1
$ mount -v -o offset=$(( 512 * 1064960 )),sizelimit=$(( 512 * 10960896 )) 2025-05-13-raspios-bookworm-arm64.img img2
```

Now you can modify the partitions as needed, and the changes will be reflected in the image file. **If you don't intend to make any modifications, like to the boot partition, include the `-r` option to mount the image read-only.**
