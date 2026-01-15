POSITION_MAP = {
    "ST": ["CF", "ST"],
    "WG": ["LW", "RW", "LWF", "RWF"],
    "CAM/10": ["AMF", "LAMF", "RAMF"],
    "CDM/6": ["DMF", "LDMF", "RDMF"],
    "CM/8": ["CMF", "LCMF", "RCMF", "LCMF3", "RCMF3"],
    "FB": ["LB", "RB", "LWB", "RWB", "LB5", "RB5"],
    "CB": ["CB", "LCB", "RCB", "LCB3", "RCB3"],
    "GK": ["GK"]
}

# Authentication
DEFAULT_PASSWORD = "PILOT26"

# UI Constants
LOGO_PATH = "best_xi_logo.png"
DISCLAIMER = (
    "Best.XI is not affiliated with or endorsed by any data provider. "
    "Users must upload data they have the legal right to use."
)

# Tab Configuration
TABS_CONFIG = {
    "App": None,
    "User Manual": "USER_MANUAL.md",
    "FAQ": "FAQ.md",
    "User Agreement": "USER_AGREEMENT.md"
}

# Scoring Constants
NEGATIVE_METRICS = [
    "Losses (total)", "Losses (own half)", "Fouls", 
    "Yellow cards", "Red cards", "Conceded goals", 
    "Shots against", "Offsides", "xCG", "% Losses (own half)"
]

# Visualization Constants
RADAR_COLORS = [
    '#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e',
    '#e6ab02', '#a6761d', '#666666', '#377eb8', '#ff7f00'
]