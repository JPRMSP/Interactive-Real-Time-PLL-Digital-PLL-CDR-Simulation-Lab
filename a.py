import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Interactive PLL & CDR Simulator", layout="wide")

st.title("🔶 Interactive Real-Time PLL, Digital PLL & CDR Simulation Lab")
st.write("Fully syllabus-aligned project for Phase Locked Loops (FI 9042) — Reg 2021")

# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

def simulate_pll(Kpd, Kvco, Fref, loop_filter, noise_level, steps=2000):
    dt = 1e-4
    phase_ref = 0
    phase_vco = 0
    freq_vco = Fref

    pd_out_list = []
    lf_out_list = []
    vco_freq_list = []

    lf_state = 0

    for _ in range(steps):
        phase_ref += 2*np.pi*Fref*dt
        phase_vco += 2*np.pi*freq_vco*dt

        pd_out = Kpd * np.sin(phase_ref - phase_vco)
        pd_out += noise_level * np.random.randn()

        lf_state = lf_state + loop_filter * pd_out
        vco_control = lf_state
        
        freq_vco = Fref + Kvco * vco_control

        pd_out_list.append(pd_out)
        lf_out_list.append(lf_state)
        vco_freq_list.append(freq_vco)

    return pd_out_list, lf_out_list, vco_freq_list


def simulate_dpll(delay, steps=1000):
    inp = np.sin(np.linspace(0, 40, steps))
    delayed = np.roll(inp, int(delay))
    return inp, delayed


def simulate_cdr(jitter_amp, steps=1000):
    data = np.random.choice([0, 1], steps)
    clock = (np.sin(np.linspace(0, 50, steps)) > 0).astype(int)
    jitter = jitter_amp * np.random.randn(steps)
    recovered = (np.sin(np.linspace(0, 50, steps) + jitter) > 0).astype(int)
    return data, clock, recovered


# --------------------------------------------------------------
# Sidebar Controls
# --------------------------------------------------------------

st.sidebar.header("PLL Parameters")
Kpd = st.sidebar.slider("Phase Detector Gain (Kpd)", 0.1, 10.0, 3.0)
Kvco = st.sidebar.slider("VCO Gain (Kvco)", 0.1, 30.0, 10.0)
Fref = st.sidebar.slider("Reference Frequency", 1.0, 20.0, 5.0)
loop_filter = st.sidebar.slider("Loop Filter Constant", 0.001, 0.1, 0.01)
noise_level = st.sidebar.slider("Noise Level", 0.0, 0.5, 0.05)

st.sidebar.header("Digital PLL")
delay = st.sidebar.slider("Digital Delay (samples)", 1, 100, 20)

st.sidebar.header("CDR Settings")
jitter_amp = st.sidebar.slider("Jitter Amplitude", 0.0, 1.0, 0.2)


# --------------------------------------------------------------
# PLL Simulation
# --------------------------------------------------------------

st.subheader("📌 Analog PLL Simulation (Phase Detector → Loop Filter → VCO)")

pd_out, lf_out, vco_freq = simulate_pll(Kpd, Kvco, Fref, loop_filter, noise_level)

fig, ax = plt.subplots(3, 1, figsize=(10, 7))
ax[0].plot(pd_out)
ax[0].set_title("Phase Detector Output")
ax[1].plot(lf_out)
ax[1].set_title("Loop Filter Response")
ax[2].plot(vco_freq)
ax[2].set_title("VCO Frequency Evolution")

st.pyplot(fig)


# --------------------------------------------------------------
# Digital PLL / Tanlock Simulation
# --------------------------------------------------------------

st.subheader("📌 Digital PLL / Tanlock Loop Demonstration")

inp, delayed = simulate_dpll(delay)

fig2, ax2 = plt.subplots(1, 1, figsize=(10, 3))
ax2.plot(inp, label="Input")
ax2.plot(delayed, label="Delayed")
ax2.legend()

st.pyplot(fig2)


# --------------------------------------------------------------
# CDR Simulation  (FIXED)
# --------------------------------------------------------------

st.subheader("📌 Clock and Data Recovery (CDR) Simulation")

data, clk, recovered = simulate_cdr(jitter_amp)

x = np.arange(200)       # <-- FIXED (Explicit x-axis)

fig3, ax3 = plt.subplots(1, 1, figsize=(10, 3))
ax3.step(x, data[:200], label="Data")
ax3.step(x, clk[:200], label="Clock")
ax3.step(x, recovered[:200], label="Recovered Clock")
ax3.legend()

st.pyplot(fig3)

st.success("Simulation completed successfully!")
