#define max_cost 5
#define num_nodes 4

typedef path {
    byte cost = max_cost;
    byte length = 0;
    byte nodes[3] = {num_nodes, num_nodes, num_nodes}
}

chan t1 = [1] of {path}
chan cn2n1 = [1] of {path}
chan t2 = [1] of {path}
chan cn3n2 = [1] of {path}
chan t3 = [1] of {path}
chan cn1n3 = [1] of {path}

ltl converges {eventually always ((len(t1) == 0) && (len(cn2n1) == 0) && (len(t2) == 0) && (len(cn3n2) == 0) && (len(t3) == 0) && (len(cn1n3) == 0))}
/*ltl converges {always eventually ((len(t1) > 0) || (len(cn2n1) > 0) || (len(t2) > 0) || (len(cn3n2) > 0) || (len(t3) > 0) || (len(cn1n3) > 0))}*/

active proctype t() {
    path p1;
    p1.cost = 3;
    t1 ! p1;
    path p2;
    p2.cost = 3;
    t2 ! p2;
    path p3;
    p3.cost = 3;
    t3 ! p3;
}

active proctype n1() {
    byte x;
    path p;
    path paths[2];
    byte cmi = 255;
    byte cmi_old = 255;
    byte min_old = max_cost;
    byte min;
    byte cont_n2[max_cost] = {0, 0, 1, 2, 3};

    do
    ::  t1 ? p;
        x = p.cost;
        if
        ::  ((p.length < num_nodes - 1) && (1 != p.nodes[0]) && (1 != p.nodes[1]));
            paths[0].cost = x;
            paths[0].length = p.length + 1;
            paths[0].nodes[0] = p.nodes[0];
            paths[0].nodes[1] = p.nodes[1];
            paths[0].nodes[2] = p.nodes[2];
            paths[0].nodes[p.length] = 1;
        ::  else;
            paths[0].cost = max_cost;
            paths[0].length = 0;
            paths[0].nodes[0] = num_nodes;
            paths[0].nodes[1] = num_nodes;
            paths[0].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 0)));
            min_old = min;
            cmi_old = cmi;
            cn1n3 ! paths[cmi]
        ::  else
        fi
    ::  cn2n1 ? p;
        x = cont_n2[p.cost];
        if
        ::  ((p.length < num_nodes - 1) && (1 != p.nodes[0]) && (1 != p.nodes[1]));
            paths[1].cost = x;
            paths[1].length = p.length + 1;
            paths[1].nodes[0] = p.nodes[0];
            paths[1].nodes[1] = p.nodes[1];
            paths[1].nodes[2] = p.nodes[2];
            paths[1].nodes[p.length] = 1;
        ::  else;
            paths[1].cost = max_cost;
            paths[1].length = 0;
            paths[1].nodes[0] = num_nodes;
            paths[1].nodes[1] = num_nodes;
            paths[1].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 1)));
            min_old = min;
            cmi_old = cmi;
            cn1n3 ! paths[cmi]
        ::  else
        fi
    od
}

active proctype n2() {
    byte x;
    path p;
    path paths[2];
    byte cmi = 255;
    byte cmi_old = 255;
    byte min_old = max_cost;
    byte min;
    byte cont_n3[max_cost] = {0, 0, 1, 2, 3};

    do
    ::  t2 ? p;
        x = p.cost;
        if
        ::  ((p.length < num_nodes - 1) && (2 != p.nodes[0]) && (2 != p.nodes[1]));
            paths[0].cost = x;
            paths[0].length = p.length + 1;
            paths[0].nodes[0] = p.nodes[0];
            paths[0].nodes[1] = p.nodes[1];
            paths[0].nodes[2] = p.nodes[2];
            paths[0].nodes[p.length] = 2;
        ::  else;
            paths[0].cost = max_cost;
            paths[0].length = 0;
            paths[0].nodes[0] = num_nodes;
            paths[0].nodes[1] = num_nodes;
            paths[0].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 0)));
            min_old = min;
            cmi_old = cmi;
            cn2n1 ! paths[cmi]
        ::  else
        fi
    ::  cn3n2 ? p;
        x = cont_n3[p.cost];
        if
        ::  ((p.length < num_nodes - 1) && (2 != p.nodes[0]) && (2 != p.nodes[1]));
            paths[1].cost = x;
            paths[1].length = p.length + 1;
            paths[1].nodes[0] = p.nodes[0];
            paths[1].nodes[1] = p.nodes[1];
            paths[1].nodes[2] = p.nodes[2];
            paths[1].nodes[p.length] = 2;
        ::  else;
            paths[1].cost = max_cost;
            paths[1].length = 0;
            paths[1].nodes[0] = num_nodes;
            paths[1].nodes[1] = num_nodes;
            paths[1].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 1)));
            min_old = min;
            cmi_old = cmi;
            cn2n1 ! paths[cmi]
        ::  else
        fi
    od
}

active proctype n3() {
    byte x;
    path p;
    path paths[2];
    byte cmi = 255;
    byte cmi_old = 255;
    byte min_old = max_cost;
    byte min;
    byte cont_n1[max_cost] = {0, 0, 1, 2, 3};

    do
    ::  t3 ? p;
        x = p.cost;
        if
        ::  ((p.length < num_nodes - 1) && (3 != p.nodes[0]) && (3 != p.nodes[1]));
            paths[0].cost = x;
            paths[0].length = p.length + 1;
            paths[0].nodes[0] = p.nodes[0];
            paths[0].nodes[1] = p.nodes[1];
            paths[0].nodes[2] = p.nodes[2];
            paths[0].nodes[p.length] = 3;
        ::  else;
            paths[0].cost = max_cost;
            paths[0].length = 0;
            paths[0].nodes[0] = num_nodes;
            paths[0].nodes[1] = num_nodes;
            paths[0].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 0)));
            min_old = min;
            cmi_old = cmi;
            cn3n2 ! paths[cmi]
        ::  else
        fi
    ::  cn1n3 ? p;
        x = cont_n1[p.cost];
        if
        ::  ((p.length < num_nodes - 1) && (3 != p.nodes[0]) && (3 != p.nodes[1]));
            paths[1].cost = x;
            paths[1].length = p.length + 1;
            paths[1].nodes[0] = p.nodes[0];
            paths[1].nodes[1] = p.nodes[1];
            paths[1].nodes[2] = p.nodes[2];
            paths[1].nodes[p.length] = 3;
        ::  else;
            paths[1].cost = max_cost;
            paths[1].length = 0;
            paths[1].nodes[0] = num_nodes;
            paths[1].nodes[1] = num_nodes;
            paths[1].nodes[2] = num_nodes;
        fi
        x = 0;
        min = 255;
        do
        ::  (x < 2);
            if
            ::  (paths[x].cost < min) -> cmi = x; min = paths[x].cost
            ::  else
            fi;
            x = x + 1;
        ::  (x >= 2) -> break
        od
        if
        ::  (cmi_old != cmi && min != min_old) || (cmi_old == cmi && (min < min_old || (min >= min_old && cmi_old == 1)));
            min_old = min;
            cmi_old = cmi;
            cn3n2 ! paths[cmi]
        ::  else
        fi
    od
}
