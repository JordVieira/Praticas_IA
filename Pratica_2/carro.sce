clc;
close;

fls=loadfls('carro2'); //carrega o arquivo carro2.fls diretamente no workspace para a variável chamada 'fls'

figure(1);
plotvar(fls,"input",[1 2]); 

figure(2);
plotvar(fls,"output",1); 

figure(3);
plotsurf(fls,[1 2], 1);


//scf();clf();
//plotsurf(fls,[1 2],1);

//scf();clf();
//plotsurf(fls,1,1,[0 50]);

//scf();clf();
//plotsurf(fls)
