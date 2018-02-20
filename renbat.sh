#!/bin/bash

let count=0

for i in *.patch; do
	let count++;
	echo -n $count ": " $i " ";
	a=`printf pcicap-%02d.39.patch $count`;
	mv $i $a;
	grep Subject $a;
done

