commit 609146fdb319cebce93be550938ab852f7bade90
Author: Arnd Bergmann <arnd@arndb.de>
Date:   Wed Jun 2 14:28:52 2010 +0200

    ipmi: autoconvert trivial BKL users to private mutex
    
    All these files use the big kernel lock in a trivial
    way to serialize their private file operations,
    typically resulting from an earlier semi-automatic
    pushdown from VFS.
    
    None of these drivers appears to want to lock against
    other code, and they all use the BKL as the top-level
    lock in their file operations, meaning that there
    is no lock-order inversion problem.
    
    Consequently, we can remove the BKL completely,
    replacing it with a per-file mutex in every case.
    Using a scripted approach means we can avoid
    typos.
    
    file=$1
    name=$2
    if grep -q lock_kernel ${file} ; then
        if grep -q 'include.*linux.mutex.h' ${file} ; then
                sed -i '/include.*<linux\/smp_lock.h>/d' ${file}
        else
                sed -i 's/include.*<linux\/smp_lock.h>.*$/include <linux\/mutex.h>/g' ${file}
        fi
        sed -i ${file} \
            -e "/^#include.*linux.mutex.h/,$ {
                    1,/^\(static\|int\|long\)/ {
                         /^\(static\|int\|long\)/istatic DEFINE_MUTEX(${name}_mutex);
    
    } }"  \
        -e "s/\(un\)*lock_kernel\>[ ]*()/mutex_\1lock(\&${name}_mutex)/g" \
        -e '/[      ]*cycle_kernel_lock();/d'
    else
        sed -i -e '/include.*\<smp_lock.h\>/d' ${file}  \
                    -e '/cycle_kernel_lock()/d'
    fi
    
    Signed-off-by: Arnd Bergmann <arnd@arndb.de>
    Acked-by: Corey Minyard <cminyard@mvista.com>
    Cc: openipmi-developer@lists.sourceforge.net


