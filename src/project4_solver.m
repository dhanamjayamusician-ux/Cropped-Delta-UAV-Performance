% Project 4: Trim, Thrust Required and Power Required of a 3.5 kg Cropped Delta Wing UAV
% Steady level flight, sea level.  Run from MATLAB: project4_solver
clear; clc; close all;

%% 1. Given data
m = 3.5; g = 10.0; W = m*g; rho = 1.225;
Cr = 0.9; Ct = 0.15; b = 1.5; e = 0.89;
CD0 = 0.03; Cm0 = 0.01;
CL_alpha = 2.92; CL_de = 0.265;
Cm_alpha = -0.292; Cm_de = -0.4;

%% 2. Geometry
lambda = Ct/Cr;
S  = (b/2)*Cr*(1 + lambda);
AR = b^2/S;
k  = 1/(pi*e*AR);
fprintf('lambda = %.4f, S = %.4f m^2, AR = %.4f, k = %.5f\n\n', lambda, S, AR, k);

%% 3. Trim sweep
alpha_deg = 0:0.5:12;
alpha = alpha_deg*pi/180;
N = numel(alpha);
de = zeros(1,N); CL = zeros(1,N); V = zeros(1,N); CD = zeros(1,N);
Tr = zeros(1,N); Pr = zeros(1,N);

for i = 1:N
    de(i) = -(Cm0 + Cm_alpha*alpha(i))/Cm_de;       % rad
    CL(i) = CL_alpha*alpha(i) + CL_de*de(i);
    V(i)  = sqrt(2*W/(rho*S*CL(i)));
    CD(i) = CD0 + k*CL(i)^2;
    Tr(i) = 0.5*rho*V(i)^2*S*CD(i);
    Pr(i) = Tr(i)*V(i);
end
LD = CL./CD;
CL15_CD = CL.^1.5./CD;
de_deg = de*180/pi;

%% 4. Table
T = table(alpha_deg', de_deg', CL', V', CD', Tr', Pr', LD', CL15_CD', ...
    'VariableNames', {'alpha_deg','delta_e_deg','CL','V_ms','CD','Tr_N','Pr_W','CL_CD','CL15_CD'});
disp(T);
writetable(T, 'results_matlab.csv');

[~, i_tr] = min(Tr); [~, i_ld] = max(LD); [~, i_pr] = min(Pr); [~, i_en] = max(CL15_CD);
fprintf('\nMin thrust: %.2f N at alpha = %.1f deg, V = %.2f m/s\n', Tr(i_tr), alpha_deg(i_tr), V(i_tr));
fprintf('Max CL/CD : %.2f at alpha = %.1f deg\n', LD(i_ld), alpha_deg(i_ld));
fprintf('Lowest power in sweep: %.2f W at alpha = %.1f deg, V = %.2f m/s\n', Pr(i_pr), alpha_deg(i_pr), V(i_pr));
fprintf('Max CL^1.5/CD in sweep: %.2f at alpha = %.1f deg\n', CL15_CD(i_en), alpha_deg(i_en));
if i_pr == N
    fprintf('NOTE: power still falling at the last sweep point (sweep boundary, not true optimum).\n');
end

%% 5. Plots (V-based panels omit alpha < 1 deg, where CL ~ 0 and V is very large)
sel = alpha_deg >= 1;
figure('Name','Cropped Delta UAV Performance','Position',[100 50 1000 1000]);

subplot(3,2,1); plot(alpha_deg, de_deg, 'o-', 'LineWidth', 1.5);
xlabel('\alpha (deg)'); ylabel('Trim \delta_e (deg)'); title('Trim elevator/elevon deflection vs \alpha'); grid on;

subplot(3,2,2); plot(alpha_deg, V, 's-', 'LineWidth', 1.5);
xlabel('\alpha (deg)'); ylabel('Velocity V (m/s)'); title('Trim velocity vs \alpha'); grid on;

subplot(3,2,3); plot(V(sel), Tr(sel), '^-', 'LineWidth', 1.5);
xlabel('Velocity V (m/s)'); ylabel('Thrust required (N)'); title('Thrust required vs V'); grid on;

subplot(3,2,4); plot(V(sel), Pr(sel), 'd-', 'LineWidth', 1.5);
xlabel('Velocity V (m/s)'); ylabel('Power required (W)'); title('Power required vs V'); grid on;

subplot(3,2,5); plot(V(sel), LD(sel), 'h-', 'LineWidth', 1.5);
xlabel('Velocity V (m/s)'); ylabel('C_L / C_D'); title('C_L/C_D vs V'); grid on;

subplot(3,2,6); plot(V(sel), CL15_CD(sel), 'p-', 'LineWidth', 1.5);
xlabel('Velocity V (m/s)'); ylabel('C_L^{1.5} / C_D'); title('C_L^{1.5}/C_D vs V'); grid on;

saveas(gcf, 'cropped_delta_uav_performance_matlab.png');
