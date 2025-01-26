
# Load libraries
import pycircos
import matplotlib.pyplot as plt
from pycircos.pycircos import Gcircle, Garc
import pandas as pd
from Bio import SeqIO

# Load the data
record = SeqIO.read("data/sequence.gb", format="genbank")
garc = Garc(arc_id="NC_000913.3", record=record, interspace=0, linewidth=0,
              facecolor="#FFFFFF00", raxis_range=(0,10), label_visible=False)

# CODE START
gcircle = Gcircle()
gcircle.add_garc(garc)
gcircle.set_garcs()

#calc CDS density
# plus_CDS  = []
# minus_CDS = []
# for feat in garc.record.features:
#     if feat.type == "CDS" and feat.strand >= 0:
#         plus_CDS.append((feat.location.parts[0].start, feat.location.parts[-1].end))
#     elif feat.strand == -1:
#         minus_CDS.append((feat.location.parts[-1].start, feat.location.parts[0].end))
# plus_density  = garc.calc_density(plus_CDS, window_size=10000)
# minus_density = garc.calc_density(minus_CDS, window_size=10000)
# gcircle.heatmap("NC_000913.3", plus_density,  raxis_range=(700,780), cmap=plt.cm.Reds)
# gcircle.heatmap("NC_000913.3", minus_density, raxis_range=(780,860), cmap=plt.cm.Blues)

# Create a figure for the plot (this is required for .py files)
plt.figure(figsize=(8, 8))  # Set the figure size
gcircle.draw()  # Draw the circos plot
plt.show()  # This is required to display the plot when running from a .py file






