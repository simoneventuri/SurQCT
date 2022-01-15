global Syst

format long
Js = 1.d0*Syst.Molecule(2).Leveljqn;
gs = Syst.Molecule(2).Levelg;

filename='/home/venturi/WORKSPACE/Air_Database/Run_0D_surQCT/database/thermo/g_N2_ForN2O_semiclassical.dat'
fileID = fopen(filename,'w');


for i =1:length(Js)
    rule = mod(Js(i),2);
    if(rule==0)
        g_semi(i) = gs(i)/12.d0;
    else
        g_semi(i) = gs(i)/6.d0;
    end
    fprintf(fileID,'%14e\n',g_semi(i));
end