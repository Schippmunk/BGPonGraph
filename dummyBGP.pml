chan t0 = [1] of {byte}
chan t1 = [1] of {byte}
chan c01 = [1] of {byte}
chan c10 = [1] of {byte}
chan c000 = [1] of {byte}

byte e = 255; /*elicited cost*/

/*ltl p1 {<>(x<e)}*/ 

active proctype t(){
	t0!10;	/* c(t0, 0)*/
	t1!100
}

active proctype n0() {
	byte e0 = 255; /*elicited cost*/
	byte x = 0;
	 byte v[2]; /*size is the out degree of n0*/
	 v[0] = 255; /*cost of accessing through target*/
	 v[1] = 255; /*cost of accessing through n1*/
	 
	 do
	 	:: t0 ? x;
	 	if
	 		:: x < v[0] -> v[0] = e0
	 		if
	 			:: x < e0 -> e0 = x; c01!e0
	 		fi
	 	fi
	 	:: c10 ? x;
	 	if
	 		:: x>0 -> x = x-1  /*it is cheaper to go from n1*/
	 	fi
	 	if
	 		:: x < v[1] -> v[1] = e0
	 		if
	 			:: x < e0 -> e0 = x; c01!e0 /*sends e to b1 trough c01*/
	 		fi
	 	fi
	 	
	 od	 		
}

active proctype n1() {
	byte x = 0;
	 byte v[2]; /*size is the out degree of n0*/
	 v[0] = 255; /*cost of accessing through target*/
	 v[1] = 255; /*cost of accessing through n1*/
	 
	 do
	 	:: t1 ? x;
	 	if
	 		:: x < v[0] -> v[0] = e
	 		if
	 			:: x < e -> e = x; c10!e
	 		fi
	 	fi
	 	:: c01 ? x;
	 	if
	 		:: x>0 -> x = x-1  /*it is cheaper to go from n1*/
	 	fi
	 	if
	 		:: x < v[1] -> v[1] = e
	 		if
	 			:: x < e -> e = x; c10!e /*sends e to b1 trough c01*/
	 		fi
	 	fi
	 od	 		
}

ltl p1 {[]e>0}



