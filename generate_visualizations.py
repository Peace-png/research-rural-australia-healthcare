#!/usr/bin/env python3
"""
Rural Australia Healthcare Research Visualizations
Generates: header_image.png, workforce_distribution.png, hypothesis_stability.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import matplotlib.patheffects as path_effects

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Color palette - warm Australian tones
COLORS = {
    'primary': '#C44536',      # Rust red (outback)
    'secondary': '#E07A5F',    # Terracotta
    'tertiary': '#F2CC8F',     # Sand
    'accent': '#3D405B',       # Dark slate
    'success': '#81B29A',      # Sage green (STABLE)
    'danger': '#E63946',       # Red (UNSTABLE)
    'background': '#F4F1DE',   # Warm cream
    'water': '#457B9D',        # Ocean blue
}

# ============================================================
# VISUALIZATION 1: Header Image - Rural Healthcare Challenge
# ============================================================

def create_header_image():
    """Create a conceptual header image showing the rural healthcare challenge"""
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=COLORS['background'])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56.25)
    ax.set_aspect('equal')
    ax.axis('off')

    # Background gradient simulation with rectangles
    for i in range(20):
        alpha = 0.1 - (i * 0.004)
        rect = FancyBboxPatch((i*5, 0), 5, 56.25,
                               boxstyle="round,pad=0",
                               facecolor=COLORS['tertiary'],
                               alpha=alpha,
                               edgecolor='none')
        ax.add_patch(rect)

    # Simplified Australia outline (stylized)
    aus_outline = np.array([
        [15, 20], [20, 35], [35, 42], [55, 43], [75, 38], [85, 30],
        [80, 22], [70, 15], [55, 12], [40, 10], [25, 12], [15, 20]
    ])
    ax.fill(aus_outline[:, 0], aus_outline[:, 1],
            color=COLORS['tertiary'], alpha=0.6, edgecolor=COLORS['accent'], linewidth=2)

    # City dots (concentrated on coast)
    cities = [(78, 32, 'Sydney', 300), (75, 28, 'Melbourne', 250),
              (82, 24, 'Brisbane', 180), (72, 20, 'Perth', 150),
              (68, 25, 'Adelaide', 100)]
    for x, y, name, size in cities:
        ax.scatter(x, y, s=size, c=COLORS['primary'], alpha=0.8, zorder=5)
        ax.text(x+1, y-2, name, fontsize=9, color=COLORS['accent'])

    # Rural areas (scattered)
    rural_coords = np.random.seed(42)  # Reproducible
    rural_x = np.random.uniform(20, 70, 25)
    rural_y = np.random.uniform(15, 38, 25)
    ax.scatter(rural_x, rural_y, s=30, c=COLORS['secondary'], alpha=0.5, marker='^', zorder=3)

    # RFDS airplane symbol
    plane_x, plane_y = 50, 35
    ax.annotate('', xy=(plane_x+5, plane_y+2), xytext=(plane_x, plane_y),
                arrowprops=dict(arrowstyle='->', color=COLORS['water'], lw=3))
    ax.text(plane_x-2, plane_y+3, 'RFDS', fontsize=8, color=COLORS['water'], fontweight='bold')

    # Legend elements
    legend_elements = [
        plt.scatter([], [], s=200, c=COLORS['primary'], label='Major Cities (Doctor Concentration)'),
        plt.scatter([], [], s=30, c=COLORS['secondary'], marker='^', label='Rural Communities'),
        plt.Line2D([0], [0], color=COLORS['water'], linewidth=3, label='RFDS Service Routes'),
    ]

    # Title and subtitle
    title = ax.text(50, 50, 'Rural Australia Healthcare Challenge',
                    fontsize=28, fontweight='bold', ha='center', color=COLORS['accent'])
    title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

    subtitle = ax.text(50, 46, 'Doctor Maldistribution, Telehealth Latency & Remote Access',
                       fontsize=14, ha='center', color=COLORS['accent'], style='italic')

    # Key stats boxes
    stats = [
        ('3,000-5,000', 'GP Shortfall'),
        ('600-800ms', 'Satellite Latency'),
        ('2-6 hours', 'Travel Time'),
    ]

    for i, (value, label) in enumerate(stats):
        x_pos = 15 + i * 30
        box = FancyBboxPatch((x_pos-10, 2), 20, 10,
                              boxstyle="round,pad=0.5",
                              facecolor='white',
                              edgecolor=COLORS['primary'],
                              alpha=0.9,
                              linewidth=2)
        ax.add_patch(box)
        ax.text(x_pos, 8.5, value, fontsize=16, fontweight='bold',
                ha='center', color=COLORS['primary'])
        ax.text(x_pos, 4.5, label, fontsize=10, ha='center', color=COLORS['accent'])

    plt.tight_layout()
    plt.savefig('/home/peace/research-rural-australia-healthcare/header_image.png',
                dpi=150, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    print("Created: header_image.png")


# ============================================================
# VISUALIZATION 2: Workforce Distribution Bar Chart
# ============================================================

def create_workforce_distribution():
    """Create bar chart showing city vs rural doctor distribution"""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    # Data based on research findings (maldistribution)
    categories = ['Major Cities', 'Inner Regional', 'Outer Regional', 'Remote', 'Very Remote']
    population_pct = [72, 18, 6, 2.5, 1.5]  # Approximate population distribution
    doctors_per_1000 = [4.2, 2.8, 2.1, 1.4, 0.9]  # Doctors per 1000 people

    x = np.arange(len(categories))
    width = 0.35

    # Population bars
    bars1 = ax.bar(x - width/2, population_pct, width, label='% Population',
                   color=COLORS['tertiary'], edgecolor=COLORS['accent'], linewidth=1.5)

    # Doctors per 1000 (scaled for visualization)
    bars2 = ax.bar(x + width/2, [d*15 for d in doctors_per_1000], width,
                   label='Doctors per 1000 (scaled)',
                   color=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars1, population_pct):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}%', ha='center', fontsize=10, fontweight='bold')

    for bar, val in zip(bars2, doctors_per_1000):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}', ha='center', fontsize=10, fontweight='bold')

    # Styling
    ax.set_xlabel('Geographic Classification', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population % / Doctor Rate (scaled)', fontsize=12, fontweight='bold')
    ax.set_title('Healthcare Workforce Maldistribution in Australia',
                 fontsize=16, fontweight='bold', color=COLORS['accent'], pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend(loc='upper right', fontsize=11)

    # Add annotation box
    textstr = 'Gap: 3,000-5,000 GPs\nneeded in rural areas'
    props = dict(boxstyle='round', facecolor=COLORS['success'], alpha=0.3)
    ax.text(0.75, 0.85, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props, fontweight='bold')

    # Grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('/home/peace/research-rural-australia-healthcare/workforce_distribution.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created: workforce_distribution.png")


# ============================================================
# VISUALIZATION 3: Hypothesis Stability Chart
# ============================================================

def create_hypothesis_stability():
    """Create radar/bar chart showing stability scores for 5 hypotheses"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='white')

    # Hypothesis data (from Ideologist + Simulator validation)
    hypotheses = [
        'Bioluminescence\nProtocol',
        'Mycelium\nNetwork',
        'Swell\nPrediction',
        'Dark\nClinics',
        'Conclave\nEffect'
    ]

    # Stability scores (0-1 scale based on simulation results)
    stability_scores = [0.93, 0.9988, 0.25, 0.35, 0.88]
    coherence_scores = [0.93, 0.9988, 0.15, 0.20, 0.85]

    # Simulation models
    models = ['Kuramoto', 'Coupled Network', 'Forced Oscillator', 'Relaxation', 'Game-theoretic']
    status = ['STABLE', 'STABLE', 'UNSTABLE', 'UNSTABLE', 'STABLE']
    status_colors = [COLORS['success'], COLORS['success'], COLORS['danger'], COLORS['danger'], COLORS['success']]

    # LEFT: Bar chart
    x = np.arange(len(hypotheses))
    width = 0.35

    bars1 = ax1.bar(x - width/2, stability_scores, width, label='Stability Score',
                    color=[c for c in status_colors], alpha=0.8, edgecolor=COLORS['accent'])
    bars2 = ax1.bar(x + width/2, coherence_scores, width, label='Coherence Score',
                    color=[c for c in status_colors], alpha=0.4, edgecolor=COLORS['accent'])

    ax1.set_ylabel('Score (0-1)', fontsize=12, fontweight='bold')
    ax1.set_title('Hypothesis Stability Scores', fontsize=14, fontweight='bold',
                  color=COLORS['accent'], pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(hypotheses, fontsize=10)
    ax1.set_ylim(0, 1.1)
    ax1.legend(loc='upper right')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.7)

    # Add status labels
    for i, (bar, stat, col) in enumerate(zip(bars1, status, status_colors)):
        ax1.text(bar.get_x() + bar.get_width()/2, 1.02, stat,
                ha='center', fontsize=9, fontweight='bold', color=col)

    # RIGHT: Radar chart
    angles = np.linspace(0, 2*np.pi, len(hypotheses), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    values_stable = stability_scores + stability_scores[:1]
    values_coherence = coherence_scores + coherence_scores[:1]

    ax2 = plt.subplot(122, projection='polar')
    ax2.plot(angles, values_stable, 'o-', linewidth=2, label='Stability',
             color=COLORS['primary'])
    ax2.fill(angles, values_stable, alpha=0.25, color=COLORS['primary'])
    ax2.plot(angles, values_coherence, 'o-', linewidth=2, label='Coherence',
             color=COLORS['water'])
    ax2.fill(angles, values_coherence, alpha=0.25, color=COLORS['water'])

    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(hypotheses, fontsize=9)
    ax2.set_ylim(0, 1)
    ax2.set_title('Simulation Validation Radar', fontsize=14, fontweight='bold',
                  color=COLORS['accent'], pad=20)
    ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

    # Add model type annotations
    ax2.annotate('Models:\nKuramoto\nCoupled\nForced\nRelaxation\nGame-theory',
                 xy=(0.5, -0.15), xycoords='axes fraction',
                 ha='center', fontsize=8, color=COLORS['accent'])

    plt.tight_layout()
    plt.savefig('/home/peace/research-rural-australia-healthcare/hypothesis_stability.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("Created: hypothesis_stability.png")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Generating Rural Australia Healthcare Visualizations")
    print("=" * 60)
    print()

    create_header_image()
    create_workforce_distribution()
    create_hypothesis_stability()

    print()
    print("=" * 60)
    print("All visualizations generated successfully!")
    print("Output directory: /home/peace/research-rural-australia-healthcare/")
    print("=" * 60)
