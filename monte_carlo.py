import numpy as np

P_Aptitude = {True: 0.8, False: 0.2}
P_Coding = {True: 0.5, False: 0.5}

P_Given_A_C = {
    (True, True): {True: 0.9, False: 0.1},   
    (True, False): {True: 0.7, False: 0.3},  
    (False, True): {True: 0.6, False: 0.4},  
    (False, False): {True: 0.3, False: 0.7}, 
}

P_Given_J = {
    True: {True: 0.8, False: 0.2},  
    False: {True: 0.2, False: 0.8}, 
}

def monte_carlo_simulation(num_samples=10000):
    count_grade_good = 0
    count_evidence = 0

    for _ in range(num_samples):

        aptitude = np.random.rand() < P_Aptitude[True]

        coding = np.random.rand() < P_Coding[True]

        p_g_given_a_c = P_Given_A_C[(aptitude, coding)]
        grade = np.random.rand() < p_g_given_a_c[True]

        p_j_given_g = P_Given_J[grade]
        go_for_job = np.random.rand() < p_j_given_g[True]

        if aptitude and coding:  
            count_evidence += 1
            if grade:  
                count_grade_good += 1

    if count_evidence == 0:
        return 0  
    return count_grade_good / count_evidence

estimated_probability = monte_carlo_simulation()
print(f"Estimated P(Grade=Good | Aptitude=Yes, Coding=Yes): {estimated_probability}")