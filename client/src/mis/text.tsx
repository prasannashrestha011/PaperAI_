export const testResult: string = `
This paper presents a novel Discrete-Action Deep Q-Network (DQN) approach for scheduling Energy Storage Systems (ESS) in residential households with the primary objective of minimizing energy costsThe reward function is defined as:

$$
R(s_t, a_t) = -C_\text{import}(s_t, a_t) + C_\text{export}(s_t, a_t) - \lambda U(s_t, a_t)
$$

where:
- \(C_\text{import}\) is the cost of importing energy,
- \(C_\text{export}\) is the reward from exporting energy,
- \(U(s_t, a_t)\) is the system unbalance penalty,
- \(\lambda\) is a weighting factor.

The state representation includes:

$$
s_t = \{ \text{SoC}_t, \Delta E_t, p_\text{import}^{t+1}, p_\text{export}^{t+1} \}
$$

The action space is discretized as:

$$
A = \{-1, -0.75, -0.5, 0, 0.5, 0.75, 1\}
$$

The Q-value update equation:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \Big[ r_t + \gamma \max_a Q(s_{t+1}, a) - Q(s_t, a_t) \Big]
$$

Additional formulas:

- Quadratic formula: \( x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \)
- Euler's identity: \( e^{i\pi} + 1 = 0 \)
- Matrix multiplication:

$$
\mathbf{C} = \mathbf{A} \mathbf{B}, \quad
C_{ij} = \sum_k A_{ik} B_{kj}
$$

- Summation and integral:

$$
\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}, \\quad
\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
$$
`;

export const testCitations = [
  "This paper presents a Discrete-Action Deep Q-Network (DQN) approach for scheduling Energy Storage Systems (ESS) to optimize energy costs for residential households.",
  "With growing demand for electric energy, and limitations on clean sources of energy, managing energy on the demand side has played a significant role in enabling sustainable growth of energy systems [1, 2].",
  "Energy demand reduction or shifting from peak to off-peak period has played a significant role in avoiding instability in the power system and avoiding situations leading to blackouts.",
  "Solving for optimum energy scheduling is inherently complex due to the interplay of several factors such as uncertainty of energy demand and renewable generation, the large-scale nature of the system, conflicting economic, strict technical and regulatory requirements.",
  "However, from the perspective of the user, it can be inconvenient, as shifting or shedding of energy usage requires their active participation to maintain economic benefits.",
  "A common approach to overcome this issue has been the integration of Distributed Energy Resources (DER), such as solar and ESS with an energy management system (EMS) on individual households [6].",
  "In this paper, the energy scheduling problem for an individual household is formulated as an Markov Decision Process (MDP) from a user perspective. The objective is to find the optimal scheduling of an hour ahead energy, to minimize the cost of energy utilized based on the varying price of the energy throughout the day.",
  "State definition: The system state at time step t is represented as a vector S_t = {S_t^{surplus}, S_t^{SoC}, P_t^{import}, P_t^{export}}. The vector encapsulates 4 different pieces of information: S_t^{surplus} indicates the difference in predicted generation and demand, S_t^{surplus} = G_t^{pred} - D_t^{pred}; S_t^{SoC} is the current state of charge of the battery; and P_t^{import}, P_t^{export} represented the import and export price of the energy for the next hour, here the price can be a predicted real-time price or time of use (ToU) tariff.",
  "Action Space: Based on the state S_t, the a_t represents the decision to import or export energy for the next hour. The user can make money by importing the energy at a lower import price and the export or using battery when the import price is high. Action taken can be constrained as -P_max^{export} <= a_t <= P_max^{import}, where -P_max^{export} and P_max^{import} are the maximum allowable energy export and import, which is the maximum charging or discharging from the battery, respectively. As suggested by [14], the action is discretized into predefined steps.",
  "The input to the proposed architecture of the RL model has 9 possible actions which range from -1 to 1, such that the action space is normalized, however the action can range to n different actions that can be taken, and the total action steps can be written as: A = {a_1, a_2, a_3 ... a_n}.",
  "The proposed model normalizes the state based on the maximum allowable actions defined by the policy, enabling effective state representation and decision-making.",
  "Reward Function: The reward R_t at each time step t consists of two components are defined as, R_t = R_{cost} + R_{unbalance}.",
];
