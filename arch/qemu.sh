qemu-system-x86_64 \
    -drive file=img.cow,format=qcow2 \
    -m 4G \
    -enable-kvm -cpu host,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time -smp 8 \
    -vga qxl -device virtio-serial-pci -spice unix=on,addr=/tmp/vm_spice.socket,disable-ticketing=on -device virtserialport,chardev=spicechannel0,name=com.redhat.spice.0 -chardev spicevmc,id=spicechannel0,name=vdagent \
    -audio spice,model=hda