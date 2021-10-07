#BeginMacro(qshock)
6

#BeginMacro(long)
2.8
#EndMacro

#BeginMacro(q)
2
#EndMacro

#BeginMacro(delta)
0.1
#EndMacro

#BeginMacro(k)
1.5
#EndMacro

#BeginMacro(inicia)
zz
#EndMacro

#BeginMacro(mirar_arriba)
(0,0,1)=(-1,0,1) and (0,0,1)!=(-2,0,1) and (0,0,1)!=(0,-1,1) and (0,0,1)!=(0,1,1) and (0,0,1)!=(1,0,1)
#EndMacro

#BeginMacro(mirar_abajo)
(0,0,1)=(1,0,1)  and (0,0,1)!=(2,0,1) and (0,0,1)!=(0,-1,1) and (0,0,1)!=(0,1,1) and (0,0,1)!=(-1,0,1)
#EndMacro

#BeginMacro(mirar_derecha)
(0,0,1)=(0,1,1)  and (0,0,1)!=(0,2,1) and (0,0,1)!=(-1,0,1) and (0,0,1)!=(1,0,1) and (0,0,1)!=(0,-1,1)
#EndMacro

#BeginMacro(mirar_izquierda)
(0,0,1)=(0,-1,1)  and (0,0,1)!=(0,-2,1) and (0,0,1)!=(-1,0,1) and (0,0,1)!=(1,0,1) and (0,0,1)!=(0,1,1)
#EndMacro