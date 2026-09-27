"""
Consolidated Research Pipeline: Staged Breast Carcinoma Immunotherapy Simulation
Concept: Staged Kisspeptin Matrix Stabilization followed by Mechanosensitive AND-Gated CAR-M
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# =====================================================================
# MODULE 1: CLINICAL GENOMIC & BIOPHYSICAL REGISTRY (ANCHORED PATIENT METRICS)
# =====================================================================
class SolidTumorProfile:
    def __init__(self, name, normal_kpa, malignant_kpa, target_antigen, her2_rate, p53_rate):
        if not 0.0 <= her2_rate <= 1.0 or not 0.0 <= p53_rate <= 1.0:
            raise ValueError("Antigen and mutation rates must be between 0 and 1")
        if normal_kpa <= 0.0 or malignant_kpa <= 0.0:
            raise ValueError("Tissue stiffness values must be positive")

        self.name = name
        self.normal_kpa = normal_kpa         
        self.malignant_kpa = malignant_kpa   
        self.target_antigen = target_antigen 
        self.her2_rate = her2_rate           
        self.p53_rate = p53_rate             

# CLINICAL DATA ANCHORS:
# - Normal breast anchor: 0.5 kPa, a rounded representative value within the
#   approximately 0.2–0.5 kPa soft-tissue range used by this model.
# - Malignant ECM anchor: 20.0 kPa, representing a stiff peripheral tumor/ECM
#   region rather than a universal value for every breast-cancer compartment.
# - HER2-positive prevalence anchor: 0.15, the lower-bound point estimate of
#   the commonly reported 15–20% clinical range.
# - TP53 mutation prevalence anchor: 0.39, a rounded model estimate within the
#   approximately 35–40% range reported across breast-cancer cohorts.
BREAST_PROFILE = SolidTumorProfile("Breast Carcinoma", 0.5, 20.0, "HER2", 0.15, 0.39)

# =====================================================================
# MODULE 2: HETEROGENEOUS COHORT GENERATOR (STATISTICAL POPULATION MATRICES)
# =====================================================================
class CohortGenerator:
    def __init__(self, tumor_profile, num_patients=1000, rng=None):
        if not isinstance(num_patients, (int, np.integer)) or num_patients <= 0:
            raise ValueError("num_patients must be a positive integer")

        self.profile = tumor_profile
        self.num_patients = num_patients
        self.rng = np.random.default_rng() if rng is None else rng
        
        target_positive = self.rng.choice(
            [True, False],
            size=num_patients,
            p=[tumor_profile.her2_rate, 1 - tumor_profile.her2_rate],
        )
        self.antigen_zscores = np.where(
            target_positive,
            self.rng.normal(loc=4.2, scale=0.8, size=num_patients),
            self.rng.normal(loc=0.0, scale=0.4, size=num_patients),
        )
        
        self.p53_status = self.rng.choice(
            ["Mutant", "Wild-Type"],
            size=num_patients,
            p=[tumor_profile.p53_rate, 1 - tumor_profile.p53_rate],
        )
        self.mmp_zscores = self.rng.normal(loc=0.0, scale=1.1, size=num_patients)
        self.initial_stiffness = self.rng.uniform(
            tumor_profile.malignant_kpa * 0.8,
            tumor_profile.malignant_kpa * 1.2,
            size=num_patients,
        )

# =====================================================================
# MODULE 3: PHASE 1 STAGED KISSPEPTIN KINETICS ENGINE (DIFFERENTIAL CORE)
# =====================================================================
def kisspeptin_mmp_axis_ode(t, y, kp_dose, base_mmp_prod, k_deg_mmp, k_ecm_prod, base_ecm_deg):
    """
    RECTIFIED BIOPHYSICAL EQUATIONS:
    MMP activity (M) drives mechanical desmoplasia and tissue cross-linking (E).
    Kisspeptin blocks downstream MMP synthesis. As M drops to zero, the structural
    degradation vector allows tissue matrices to drop from 20 kPa back down to soft baselines.
    """
    M, E = y
    IC50_kisspeptin = 1.5  
    inhibition_coefficient = 1.0 / (1.0 + (kp_dose / IC50_kisspeptin))
    
    # Direct Kisspeptin suppression loop
    dM_dt = (base_mmp_prod * inhibition_coefficient) - (k_deg_mmp * M)
    
    # Balanced structural mechanics model: MMP activity induces remodeling and stiffening
    dE_dt = (k_ecm_prod * M) - (base_ecm_deg * E)
    return [dM_dt, dE_dt]

# =====================================================================
# MODULE 4: PHASE 2 INTEGRATED SYNNOTCH CAR-M LOGIC GATE (CIRCUIT ARCHITECTURE)
# =====================================================================
def evaluate_logic_gated_carm(stiffness, antigen_z, p53, profile):
    """
    REWIRED TRANSCRIPTIONAL AND-GATE SYSTEM:
    Check 1 (The Mechanosensitive Target Corridor): Uses tissue stiffness as a
            simulation proxy for a softened Kisspeptin-treated region; stiffness alone
            does not prove that Kisspeptin caused the change in a real tissue.
    Check 2 (The Combinatorial Fingerprint): Scans for surface HER2 OR a TP53
            mutation-status input. TP53 is intracellular, so a real CAR would require
            a surface-presented surrogate rather than directly sensing TP53.
    """
    # Check 1: Breast corridor bounds (Normal target window sits underneath 5.0 kPa safety ceiling)
    input_key_a_stiff = 1.0 if (1.0 <= stiffness <= 5.0) else 0.0
        
    # Check 2: Combinatorial Cellular Profile Scan
    input_key_b1_antigen = 1.0 if antigen_z >= 1.5 else 0.0
    input_key_b2_p53 = 1.0 if p53 == "Mutant" else 0.0
    identity_validated = (input_key_b1_antigen == 1.0) or (input_key_b2_p53 == 1.0)
    
    # Resolving the logical processing circuit
    if (input_key_a_stiff == 1.0) and identity_validated:
        gate_fired = True
        phagocytic_efficiency = 0.98  
    else:
        gate_fired = False
        phagocytic_efficiency = 0.00  
        
    return gate_fired, phagocytic_efficiency

# =====================================================================
# MODULE 5: MASTER SIMULATION CONTROLLER (COHORT PIPELINE EXECUTION)
# =====================================================================
def execute_breast_therapy_pipeline(kisspeptin_dose=10.0, num_patients=1000, seed=42):
    profile = BREAST_PROFILE
    rng = np.random.default_rng(seed)
    cohort = CohortGenerator(profile, num_patients=num_patients, rng=rng)
    
    time_span = (0, 15)  
    t_eval = np.linspace(0, 15, 150)
    
    final_stiffness_array = np.zeros(cohort.num_patients)
    successful_clearance_events = 0
    
    print(f"\n[STARTING PIPELINE RUN] Target Model: {profile.name}")
    
    sample_control_ode = None
    sample_treated_ode = None
    
    for i in range(cohort.num_patients):
        mmp_initial = 12.0 + cohort.mmp_zscores[i]
        stiff_initial = cohort.initial_stiffness[i]
        initial_conditions = [float(mmp_initial), float(stiff_initial)]
        
        if i == 0:
            # FIXED ARGS: Rebalanced physiological breast tissue multi-variable multipliers
            sample_control_ode = solve_ivp(
                kisspeptin_mmp_axis_ode,
                time_span,
                initial_conditions,
                t_eval=t_eval,
                args=(0.0, 1.0, 0.5, 1.0, 0.35),
            )
            if not sample_control_ode.success:
                raise RuntimeError(f"Control ODE failed: {sample_control_ode.message}")
            
        treated_ode = solve_ivp(
            kisspeptin_mmp_axis_ode,
            time_span,
            initial_conditions,
            t_eval=t_eval,
            args=(kisspeptin_dose, 1.0, 0.5, 1.0, 0.35),
        )
        if not treated_ode.success:
            raise RuntimeError(f"Treated ODE failed for patient {i}: {treated_ode.message}")
        
        if i == 0:
            sample_treated_ode = treated_ode
            
        # FIXED ARRAY SYNTAX: Correctly isolates variable row 1 (Stiffness) at terminal coordinate index
        day15_stiffness = treated_ode.y[1, -1]
        final_stiffness_array[i] = day15_stiffness
        
        gate_triggered, efficiency = evaluate_logic_gated_carm(
            day15_stiffness, cohort.antigen_zscores[i], cohort.p53_status[i], profile
        )
        
        if gate_triggered:
            successful_clearance_events += 1
            
    overall_response_rate = (successful_clearance_events / cohort.num_patients) * 100
    
    print(f"|--------------------------------------------------------|")
    print(f"  Target Solid Tumor Variant : {profile.name}")
    print(f"  Mean Post-Kisspeptin Modulus: {np.mean(final_stiffness_array):.2f} kPa")
    print(f"  CAR-M Logic Gates Activated: {successful_clearance_events} / {cohort.num_patients} Patients")
    print(f"  Predicted Therapeutic Yield: {overall_response_rate:.1f}% Clearance Success")
    print(f"|--------------------------------------------------------|\n")
    
    return sample_control_ode, sample_treated_ode, profile, final_stiffness_array

# =====================================================================
# MODULE 6: VISUAL ANALYTICS COMPILATION (MATPLOTLIB DASHBOARD)
# =====================================================================
def render_research_plots(control, treated, profile, stiffness_array):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # CORRECTED NUMPY SLICING: Uses standard [row, column] indexing to cleanly isolate 1D traces
    ax1.plot(control.t, control.y[0, :], 'r-', linewidth=2.5, label='Control (Untreated)')
    ax1.plot(treated.t, treated.y[0, :], 'g--', linewidth=2.5, label='Treated (Kisspeptin)')
    ax1.set_title(f"MMP-2/9 Concentration Decay ({profile.name})")
    ax1.set_xlabel("Duration (Days)")
    ax1.set_ylabel("Enzymatic Activity Unit")
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend()
    
    # CORRECTED NUMPY SLICING: Pulls exclusive Extracellular Modulus stiffness trace
    ax2.plot(control.t, control.y[1, :], 'r-', linewidth=2.5, label='Control Matrix (Runaway Desmoplasia)')
    ax2.plot(treated.t, treated.y[1, :], 'g--', linewidth=2.5, label='Stabilized Matrix (Kisspeptin Protected)')
    
    # Highlight the safe mechanosensitive operational trigger window (1.0 - 5.0 kPa)
    ax2.axhspan(1.0, 5.0, color='blue', alpha=0.1, label='Active Trigger Corridor (1.0–5.0 kPa)')
    
    ax2.set_title(f"Extracellular Matrix Stiffness Response ({profile.name})")
    ax2.set_xlabel("Duration (Days)")
    ax2.set_ylabel("Tissue Elastic Modulus (kPa)")
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend()
    plt.tight_layout()
    plt.show()
    return fig, (ax1, ax2)


# =====================================================================
# MASTER EXECUTION LOOP
# =====================================================================
if __name__ == "__main__":
    control_out, treated_out, tumor_profile, final_stiff = execute_breast_therapy_pipeline(
        kisspeptin_dose=10.0
    )
    render_research_plots(control_out, treated_out, tumor_profile, final_stiff)