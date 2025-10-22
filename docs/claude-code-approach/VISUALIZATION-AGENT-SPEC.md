# Visualization Agent Specification

**Purpose:** Convert research findings into clear, publication-ready visualizations that enhance understanding and decision-making.

**Capabilities:** Charts, graphs, diagrams, comparison matrices, timelines, architecture diagrams
**Output Formats:** PNG (high-res), SVG (vector), PDF (print)
**Integration:** Seamless embedding into research documents

---

## Table of Contents

1. [Agent Identity](#agent-identity)
2. [Input Specifications](#input-specifications)
3. [Visualization Types](#visualization-types)
4. [Output Standards](#output-standards)
5. [Implementation Tools](#implementation-tools)
6. [Prompt Template](#prompt-template)

---

## Agent Identity

**Role:** Data Visualization Specialist
**Expertise:**
- Statistical visualization
- Technical architecture diagrams
- Comparative analysis charts
- Time-series analysis
- Performance benchmarking visuals

**Mission:** Transform research data into visual insights that communicate complex information clearly and accurately.

---

## Input Specifications

### Data Input Format

The visualization agent expects structured data in JSON format:

```json
{
  "visualization_type": "bar_chart|line_chart|scatter|comparison_matrix|architecture_diagram|timeline|heatmap|radar_chart",
  "title": "Chart Title",
  "subtitle": "Optional subtitle for context",
  "data": {
    // Type-specific data structure (see below)
  },
  "styling": {
    "color_scheme": "professional|vibrant|monochrome|custom",
    "size": "small|medium|large|custom",
    "dpi": 300,
    "format": "png|svg|pdf"
  },
  "annotations": [
    {
      "type": "text|arrow|box",
      "content": "Annotation text",
      "position": {"x": 0, "y": 0}
    }
  ],
  "metadata": {
    "source": "Research document ID",
    "created": "ISO 8601 timestamp",
    "purpose": "What this visualization demonstrates"
  }
}
```

### Data Structures by Type

#### Bar Chart / Column Chart
```json
{
  "data": {
    "categories": ["Category 1", "Category 2", "Category 3"],
    "series": [
      {
        "name": "Series 1",
        "values": [100, 200, 150],
        "color": "#FF6B6B"
      }
    ],
    "x_axis_label": "X Axis",
    "y_axis_label": "Y Axis",
    "show_values": true
  }
}
```

#### Line Chart (Time Series)
```json
{
  "data": {
    "time_points": ["2024-01", "2024-02", "2024-03"],
    "series": [
      {
        "name": "Metric 1",
        "values": [100, 120, 115],
        "color": "#4ECDC4"
      }
    ],
    "x_axis_label": "Time",
    "y_axis_label": "Value",
    "show_markers": true,
    "trend_line": false
  }
}
```

#### Comparison Matrix
```json
{
  "data": {
    "options": ["Option A", "Option B", "Option C"],
    "criteria": [
      {
        "name": "Performance",
        "weight": 0.3,
        "scores": [8, 6, 9]
      },
      {
        "name": "Cost",
        "weight": 0.2,
        "scores": [5, 9, 7]
      }
    ],
    "scale": {
      "min": 0,
      "max": 10,
      "interpretation": "Higher is better"
    }
  }
}
```

#### Architecture Diagram
```json
{
  "data": {
    "components": [
      {
        "id": "comp1",
        "label": "Component 1",
        "type": "service|database|queue|cache",
        "position": {"x": 0, "y": 0}
      }
    ],
    "connections": [
      {
        "from": "comp1",
        "to": "comp2",
        "label": "HTTP",
        "type": "sync|async|data_flow"
      }
    ],
    "groups": [
      {
        "id": "group1",
        "label": "Container",
        "components": ["comp1", "comp2"],
        "style": "dashed|solid"
      }
    ]
  }
}
```

#### Performance Benchmark
```json
{
  "data": {
    "benchmarks": [
      {
        "name": "Tool A",
        "metrics": {
          "throughput": 1000,
          "latency_p50": 10,
          "latency_p99": 50,
          "cpu_usage": 25,
          "memory_mb": 512
        }
      }
    ],
    "baseline": "Tool A",
    "highlight_best": true
  }
}
```

#### Timeline / Gantt
```json
{
  "data": {
    "phases": [
      {
        "name": "Phase 1",
        "start": "2024-01-01",
        "end": "2024-01-31",
        "status": "completed|in_progress|planned",
        "dependencies": []
      }
    ],
    "milestones": [
      {
        "name": "Milestone 1",
        "date": "2024-01-15"
      }
    ]
  }
}
```

#### Radar Chart (Multi-dimensional Comparison)
```json
{
  "data": {
    "dimensions": ["Speed", "Reliability", "Cost", "Ease of Use", "Scalability"],
    "subjects": [
      {
        "name": "Solution A",
        "values": [8, 9, 5, 7, 8],
        "color": "#FF6B6B"
      }
    ],
    "scale": {
      "min": 0,
      "max": 10
    }
  }
}
```

---

## Visualization Types

### 1. Performance Comparison Charts

**Use case:** Comparing performance metrics across technologies/configurations

**Best for:**
- Throughput comparisons
- Latency distributions
- Resource usage (CPU, RAM, disk)
- Benchmark results

**Output example:**
```python
import matplotlib.pyplot as plt
import numpy as np

def create_performance_comparison(data):
    """
    Creates a grouped bar chart comparing performance metrics.
    """
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    technologies = data['technologies']
    metrics = data['metrics']

    x = np.arange(len(technologies))
    width = 0.2
    multiplier = 0

    for metric_name, values in metrics.items():
        offset = width * multiplier
        ax.bar(x + offset, values, width, label=metric_name)
        multiplier += 1

    ax.set_xlabel('Technology')
    ax.set_ylabel('Performance (normalized)')
    ax.set_title('Performance Comparison Across Technologies')
    ax.set_xticks(x + width)
    ax.set_xticklabels(technologies)
    ax.legend(loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig
```

### 2. Cost-Benefit Analysis Matrix

**Use case:** Visualizing trade-offs between options

**Best for:**
- Technology selection decisions
- Architecture choices
- Resource allocation decisions

**Output example:**
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_cost_benefit_matrix(data):
    """
    Creates a scatter plot with quadrant analysis.
    """
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    for option in data['options']:
        ax.scatter(option['cost'], option['benefit'],
                  s=option['size']*100, alpha=0.6,
                  label=option['name'])
        ax.annotate(option['name'],
                   (option['cost'], option['benefit']),
                   xytext=(5, 5), textcoords='offset points')

    # Add quadrant lines
    ax.axhline(y=data['benefit_threshold'], color='gray',
              linestyle='--', alpha=0.5)
    ax.axvline(x=data['cost_threshold'], color='gray',
              linestyle='--', alpha=0.5)

    # Quadrant labels
    ax.text(0.25, 0.95, 'Low Cost\nHigh Benefit',
           transform=ax.transAxes, ha='center',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

    ax.set_xlabel('Cost (normalized)')
    ax.set_ylabel('Benefit (normalized)')
    ax.set_title('Cost-Benefit Analysis Matrix')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
```

### 3. Architecture Diagrams

**Use case:** System architecture visualization

**Best for:**
- Component relationships
- Data flow
- Deployment architecture
- Network topology

**Output example:**
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def create_architecture_diagram(data):
    """
    Creates a system architecture diagram.
    """
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Component colors by type
    colors = {
        'service': '#4ECDC4',
        'database': '#FF6B6B',
        'cache': '#FFE66D',
        'queue': '#95E1D3'
    }

    # Draw components
    for comp in data['components']:
        box = FancyBboxPatch(
            (comp['x'], comp['y']), 1.5, 0.8,
            boxstyle="round,pad=0.1",
            facecolor=colors.get(comp['type'], 'lightgray'),
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(comp['x'] + 0.75, comp['y'] + 0.4,
               comp['label'],
               ha='center', va='center', fontsize=10, weight='bold')

    # Draw connections
    for conn in data['connections']:
        from_comp = next(c for c in data['components'] if c['id'] == conn['from'])
        to_comp = next(c for c in data['components'] if c['id'] == conn['to'])

        arrow = FancyArrowPatch(
            (from_comp['x'] + 1.5, from_comp['y'] + 0.4),
            (to_comp['x'], to_comp['y'] + 0.4),
            arrowstyle='->', mutation_scale=20,
            linewidth=2, color='black'
        )
        ax.add_patch(arrow)

        # Label
        mid_x = (from_comp['x'] + to_comp['x']) / 2
        mid_y = (from_comp['y'] + to_comp['y']) / 2
        ax.text(mid_x, mid_y + 0.2, conn['label'],
               ha='center', fontsize=8, style='italic',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_title('System Architecture', fontsize=16, weight='bold', pad=20)

    plt.tight_layout()
    return fig
```

### 4. Resource Utilization Timeline

**Use case:** Showing resource usage over time

**Best for:**
- Capacity planning
- Performance trends
- Bottleneck identification

**Output example:**
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def create_resource_timeline(data):
    """
    Creates a stacked area chart for resource utilization.
    """
    fig, ax = plt.subplots(figsize=(14, 6), dpi=300)

    timestamps = [datetime.fromisoformat(t) for t in data['timestamps']]

    # Stack resources
    ax.fill_between(timestamps, 0, data['cpu'],
                   label='CPU', alpha=0.7, color='#FF6B6B')
    ax.fill_between(timestamps, data['cpu'],
                   [c + m for c, m in zip(data['cpu'], data['memory'])],
                   label='Memory', alpha=0.7, color='#4ECDC4')

    # Add threshold line
    ax.axhline(y=data['threshold'], color='red',
              linestyle='--', linewidth=2, label='Capacity Threshold')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.xticks(rotation=45)

    ax.set_xlabel('Date')
    ax.set_ylabel('Resource Usage (%)')
    ax.set_title('Resource Utilization Timeline')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
```

### 5. Decision Matrix Heatmap

**Use case:** Multi-criteria decision analysis

**Best for:**
- Technology selection
- Vendor comparison
- Feature prioritization

**Output example:**
```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def create_decision_matrix(data):
    """
    Creates a heatmap for decision matrix visualization.
    """
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    # Create matrix
    matrix = np.array([[item['score'] for item in criterion['items']]
                      for criterion in data['criteria']])

    # Create heatmap
    sns.heatmap(matrix, annot=True, fmt='.1f', cmap='RdYlGn',
               xticklabels=data['options'],
               yticklabels=[c['name'] for c in data['criteria']],
               cbar_kws={'label': 'Score'},
               linewidths=0.5, linecolor='gray',
               vmin=0, vmax=10)

    ax.set_title('Multi-Criteria Decision Matrix', fontsize=14, weight='bold', pad=20)

    # Add weighted totals at bottom
    totals = []
    for i, option in enumerate(data['options']):
        total = sum(data['criteria'][j]['weight'] * matrix[j][i]
                   for j in range(len(data['criteria'])))
        totals.append(f'{total:.1f}')

    for i, total in enumerate(totals):
        ax.text(i + 0.5, len(data['criteria']) + 0.5,
               f'Total: {total}',
               ha='center', va='center', weight='bold')

    plt.tight_layout()
    return fig
```

### 6. Implementation Timeline (Gantt-style)

**Use case:** Project planning and phase visualization

**Best for:**
- Implementation roadmaps
- Dependency tracking
- Milestone visualization

**Output example:**
```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def create_implementation_timeline(data):
    """
    Creates a Gantt-style timeline chart.
    """
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)

    colors = {
        'completed': '#95E1D3',
        'in_progress': '#FFE66D',
        'planned': '#D3D3D3'
    }

    y_pos = 0
    for phase in data['phases']:
        start = datetime.fromisoformat(phase['start'])
        end = datetime.fromisoformat(phase['end'])
        duration = (end - start).days

        ax.barh(y_pos, duration, left=start, height=0.5,
               color=colors[phase['status']],
               edgecolor='black', linewidth=1)

        # Phase label
        ax.text(start + timedelta(days=duration/2), y_pos,
               phase['name'],
               ha='center', va='center', weight='bold')

        y_pos += 1

    # Add milestones
    for milestone in data['milestones']:
        date = datetime.fromisoformat(milestone['date'])
        ax.scatter(date, y_pos + 0.5, marker='D', s=200,
                  color='red', zorder=10, edgecolor='black')
        ax.text(date, y_pos + 0.8, milestone['name'],
               ha='center', fontsize=8, style='italic')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_yticks(range(len(data['phases'])))
    ax.set_yticklabels([p['name'] for p in data['phases']])
    ax.set_xlabel('Date')
    ax.set_title('Implementation Timeline', fontsize=14, weight='bold')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[k], label=k.replace('_', ' ').title())
                      for k in colors.keys()]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
```

---

## Output Standards

### File Naming Convention
```
[research-id]_[viz-type]_[description]_[version].[format]

Examples:
HW-02_bar_chart_usb_performance_v1.png
SW-02_comparison_matrix_monitoring_tools_v2.svg
SYN-01_architecture_diagram_system_overview_v1.pdf
```

### Resolution & Size Standards

| Use Case | DPI | Dimensions | Format |
|----------|-----|------------|--------|
| Research document embed | 300 | 2400×1800px | PNG |
| Presentation slides | 150 | 1920×1080px | PNG |
| Print publication | 600 | Custom | PDF |
| Web display | 96 | 1200×900px | PNG/SVG |
| Interactive | N/A | Responsive | SVG |

### Color Schemes

#### Professional (Default)
```python
COLORS_PROFESSIONAL = {
    'primary': '#2E4057',    # Dark blue-gray
    'secondary': '#4ECDC4',  # Teal
    'accent': '#FF6B6B',     # Coral red
    'success': '#95E1D3',    # Mint green
    'warning': '#FFE66D',    # Yellow
    'neutral': '#D3D3D3'     # Light gray
}
```

#### High Contrast (Accessibility)
```python
COLORS_HIGH_CONTRAST = {
    'primary': '#000000',
    'secondary': '#0066CC',
    'accent': '#CC0000',
    'success': '#008000',
    'warning': '#FF6600',
    'neutral': '#666666'
}
```

#### Print-Friendly (Grayscale-compatible)
```python
COLORS_PRINT = {
    'primary': '#333333',
    'secondary': '#666666',
    'accent': '#999999',
    'success': '#AAAAAA',
    'warning': '#555555',
    'neutral': '#DDDDDD'
}
```

### Typography Standards

```python
TYPOGRAPHY = {
    'title': {
        'fontsize': 16,
        'weight': 'bold',
        'family': 'sans-serif'
    },
    'subtitle': {
        'fontsize': 12,
        'weight': 'normal',
        'family': 'sans-serif',
        'style': 'italic'
    },
    'axis_label': {
        'fontsize': 11,
        'weight': 'normal',
        'family': 'sans-serif'
    },
    'tick_label': {
        'fontsize': 9,
        'weight': 'normal',
        'family': 'sans-serif'
    },
    'annotation': {
        'fontsize': 9,
        'weight': 'normal',
        'family': 'sans-serif',
        'style': 'italic'
    },
    'legend': {
        'fontsize': 10,
        'weight': 'normal',
        'family': 'sans-serif'
    }
}
```

---

## Implementation Tools

### Required Python Libraries

```bash
pip install matplotlib seaborn numpy pandas pillow cairosvg
```

### Matplotlib Configuration

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set global defaults
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['axes.axisbelow'] = True
```

### Visualization Pipeline

```python
class VisualizationAgent:
    """
    Main visualization agent class.
    """

    def __init__(self, output_dir='research-viz'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate(self, spec):
        """
        Generate visualization from specification.

        Args:
            spec: Dictionary containing visualization specification

        Returns:
            Path to generated file
        """
        viz_type = spec['visualization_type']

        # Route to appropriate generator
        generators = {
            'bar_chart': self._generate_bar_chart,
            'line_chart': self._generate_line_chart,
            'comparison_matrix': self._generate_comparison_matrix,
            'architecture_diagram': self._generate_architecture_diagram,
            'timeline': self._generate_timeline,
            'heatmap': self._generate_heatmap,
            'radar_chart': self._generate_radar_chart
        }

        if viz_type not in generators:
            raise ValueError(f"Unknown visualization type: {viz_type}")

        fig = generators[viz_type](spec['data'])

        # Add title and subtitle
        if 'title' in spec:
            fig.suptitle(spec['title'], fontsize=16, weight='bold')
        if 'subtitle' in spec:
            fig.text(0.5, 0.95, spec['subtitle'],
                    ha='center', fontsize=12, style='italic')

        # Add annotations
        if 'annotations' in spec:
            self._add_annotations(fig, spec['annotations'])

        # Save with metadata
        output_path = self._save_figure(fig, spec)

        plt.close(fig)

        return output_path

    def _save_figure(self, fig, spec):
        """Save figure with proper naming and format."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{spec['metadata']['source']}_{spec['visualization_type']}_{timestamp}"

        format = spec['styling'].get('format', 'png')
        filepath = os.path.join(self.output_dir, f"{filename}.{format}")

        fig.savefig(filepath, dpi=spec['styling'].get('dpi', 300),
                   bbox_inches='tight', format=format)

        return filepath
```

---

## Prompt Template

### Visualization Agent Prompt

```markdown
# VISUALIZATION AGENT: [VIZ-ID]

## Mission
Create a [visualization_type] that visualizes [specific data/finding] from research document [research-id].

## Input Data
[Provide structured data in JSON format per input specifications above]

## Visualization Requirements

### Primary Goal
[What insight should this visualization communicate?]

### Target Audience
- **Technical level:** [High/Medium/Low]
- **Domain expertise:** [Expert/Intermediate/Novice]
- **Usage context:** [Research doc/Presentation/Report/Web]

### Visual Style
- **Color scheme:** [Professional/High-contrast/Print-friendly/Custom]
- **Emphasis:** [What data points should stand out?]
- **Comparison:** [What comparisons should be obvious?]

### Annotations Needed
1. [Annotation 1: e.g., "Highlight optimal region"]
2. [Annotation 2: e.g., "Mark threshold line"]
3. [Annotation 3: e.g., "Label outliers"]

## Output Specifications

### File Details
- **Format:** [PNG/SVG/PDF]
- **Resolution:** [DPI]
- **Dimensions:** [Width × Height or "Standard"]
- **Filename:** [research-id]_[viz-type]_[description]_v[version].[format]

### Quality Checklist
- [ ] Title clearly describes what's being shown
- [ ] Axes are labeled with units
- [ ] Legend is present and clear
- [ ] Color scheme is accessible
- [ ] Annotations add clarity, not clutter
- [ ] Data is accurately represented
- [ ] Visual is self-explanatory without context

## Success Criteria
This visualization succeeds if a viewer can:
1. [Understanding goal 1]
2. [Understanding goal 2]
3. [Decision/insight they should reach]

## Notes & Context
[Any additional context about the data, caveats, or special requirements]
```

### Example: Creating a Performance Comparison

```markdown
# VISUALIZATION AGENT: VIZ-SW-02-01

## Mission
Create a bar chart comparing RAM usage of monitoring solutions from research document SW-02.

## Input Data
```json
{
  "visualization_type": "bar_chart",
  "title": "Monitoring Stack RAM Usage Comparison",
  "subtitle": "Measured on ARM64, 2GB system",
  "data": {
    "categories": ["Prometheus+Loki", "VictoriaMetrics+VictoriaLogs", "Netdata"],
    "series": [
      {
        "name": "RAM Usage (MB)",
        "values": [1500, 670, 800],
        "color": "#FF6B6B"
      }
    ],
    "x_axis_label": "Monitoring Solution",
    "y_axis_label": "RAM Usage (MB)",
    "show_values": true
  },
  "styling": {
    "color_scheme": "professional",
    "size": "medium",
    "dpi": 300,
    "format": "png"
  },
  "annotations": [
    {
      "type": "line",
      "content": "2GB System Limit",
      "position": {"y": 2000},
      "style": "dashed"
    },
    {
      "type": "text",
      "content": "87% reduction",
      "position": {"x": 1, "y": 1100}
    }
  ],
  "metadata": {
    "source": "SW-02",
    "created": "2025-01-15T10:30:00Z",
    "purpose": "Demonstrate VictoriaMetrics advantage for low-memory systems"
  }
}
```

## Visualization Requirements

### Primary Goal
Show that VictoriaMetrics+VictoriaLogs uses significantly less RAM than Prometheus+Loki, making it viable for 2GB systems.

### Target Audience
- **Technical level:** High (technical decision makers)
- **Domain expertise:** Intermediate (familiar with monitoring concepts)
- **Usage context:** Research document embedding

### Visual Style
- **Color scheme:** Professional
- **Emphasis:** Highlight VictoriaMetrics bar (make it stand out)
- **Comparison:** Clear height difference should be immediately obvious

### Annotations Needed
1. Horizontal line at 2GB showing system limit
2. Text showing percentage reduction (87%)
3. Label indicating "Recommended" on VictoriaMetrics bar

## Output Specifications

### File Details
- **Format:** PNG
- **Resolution:** 300 DPI
- **Dimensions:** 2400×1800px (4:3 ratio)
- **Filename:** SW-02_bar_chart_monitoring_ram_comparison_v1.png

### Quality Checklist
- [x] Title clearly describes comparison
- [x] Y-axis labeled with units (MB)
- [x] Values shown on top of bars
- [x] System limit line clearly visible
- [x] Recommended option visually distinct
- [x] Professional color scheme applied

## Success Criteria
This visualization succeeds if a viewer can:
1. Immediately see VictoriaMetrics uses ~half the RAM
2. Understand that Prometheus+Loki would consume 75% of system RAM
3. Recognize VictoriaMetrics as the viable choice for this constraint

## Notes & Context
- Data sourced from TrueFoundry benchmarks and community reports
- Values are approximate (documented ranges: Prometheus 1.5-2GB, VictoriaMetrics 600-750MB)
- Emphasize this is for ARM64 architecture specifically
```

---

## Integration with Research Documents

### Embedding Visualizations in Markdown

```markdown
## Performance Comparison

The following chart compares RAM usage across monitoring solutions:

![Monitoring RAM Usage Comparison](research-viz/SW-02_bar_chart_monitoring_ram_comparison_v1.png)

**Figure 1:** RAM usage comparison showing VictoriaMetrics+VictoriaLogs uses 87% less memory than Prometheus+Loki on ARM64 systems. This makes it viable for the Le Potato's 2GB constraint.

**Key insight:** The VictoriaMetrics stack leaves adequate headroom for other services, while Prometheus would consume 75% of available RAM.
```

### Figure Captioning Standards

```markdown
**Figure [N]:** [One-sentence description of what the visualization shows]

**Key insight:** [The main takeaway or decision-enabling conclusion]

**Methodology:** [How the data was collected/calculated, if relevant]

**Source:** [Research document ID or external source]
```

---

## Quality Assurance Checklist

Before finalizing any visualization:

- [ ] **Accuracy:** Data correctly represents source material
- [ ] **Clarity:** Can be understood without extensive explanation
- [ ] **Accessibility:** Color-blind friendly palette used
- [ ] **Resolution:** Meets output standard for intended use
- [ **Labeling:** All axes, legends, and annotations present
- [ ] **Consistency:** Matches style of other visuals in document
- [ ] **Self-contained:** Title and labels provide full context
- [ ] **Emphasis:** Important data points stand out appropriately
- [ ] **Simplicity:** No unnecessary visual elements (chart junk)
- [ ] **Professionalism:** Publication-ready quality

---

## Advanced Techniques

### Interactive Visualizations (Optional)

For web-based research documents, consider Plotly for interactivity:

```python
import plotly.graph_objects as go

def create_interactive_comparison(data):
    fig = go.Figure()

    for series in data['series']:
        fig.add_trace(go.Bar(
            name=series['name'],
            x=data['categories'],
            y=series['values'],
            text=series['values'],
            textposition='auto',
        ))

    fig.update_layout(
        title=data['title'],
        xaxis_title=data['x_axis_label'],
        yaxis_title=data['y_axis_label'],
        barmode='group',
        template='plotly_white'
    )

    return fig.to_html()
```

### Animation for Timeline Visualizations

```python
from matplotlib.animation import FuncAnimation

def create_animated_timeline(data):
    """Animate growth/progress over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    def update(frame):
        ax.clear()
        # Update visualization for current frame
        # ...

    anim = FuncAnimation(fig, update, frames=len(data['timepoints']),
                        interval=500, repeat=True)

    anim.save('timeline_animation.gif', writer='pillow')
```

---

## Error Handling & Edge Cases

### Missing Data
```python
def handle_missing_data(data):
    """Handle missing or incomplete data gracefully."""
    if not data:
        # Create placeholder visualization
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'Data not available',
               ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig

    # Continue with normal visualization
```

### Outliers
```python
def handle_outliers(values, threshold=3):
    """Detect and annotate outliers."""
    mean = np.mean(values)
    std = np.std(values)
    outliers = [i for i, v in enumerate(values)
               if abs(v - mean) > threshold * std]
    return outliers
```

### Scale Issues
```python
def auto_scale_axis(ax, values):
    """Automatically scale axis for readability."""
    max_val = max(values)

    if max_val > 1000:
        # Use K notation
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, p: f'{x/1000:.1f}K')
        )
    elif max_val < 0.01:
        # Use scientific notation
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
```

---

**Visualization Agent Version:** 1.0
**Last Updated:** [Date]
**Maintainer:** Research System Team
