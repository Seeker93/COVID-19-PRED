"""This file provides functions to work with our data and plot it as we desire
in an easier way
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------FEATURES SECTION ----------------

# -----------------------------------------------------------
def _sort_cluster_arrays(arrays):
  """Calculates for the given array which is their natural order:
  minimum values < ... < maxium values

  Returns the given array sorted like this.

  DEPRECATED. Was used before creating sorting cluster dictionary.
  """
  output = arrays

  for i in range(0, len(output)):
    for j in range(i+1, len(output)):
      if min(output[j]) < min(output[i]):
        output[i], output[j] = output[j], output[i]

  return output

# -----------------------------------------------------------
def _sort_cluster_dict(dictionary):
  """Calculates for the given dictionary which is their natural order:
  minimum values < ... < maxium values

  Returns the given dictionary sorted like this
  """

  output = {}

  values = {
    "min": 1000000,
    "min_name": None,
    "max": 0,
    "max_name": None,
    "middle_name": None
  }

  for k in dictionary:
    if min(dictionary[k]) < values["min"]:
      values["min"] = min(dictionary[k])
      values["min_name"] = k
    if max(dictionary[k]) > values["max"]:
      values["max"] = max(dictionary[k])
      values["max_name"] = k

  for index in dictionary:
    mini = values["min_name"]
    maxi = values["max_name"]
    if index not in [mini, maxi]:
      values["middle_name"] = index

  # Compose the output in order
  output[0] = dictionary[values["min_name"]]
  output[1] = dictionary[values["middle_name"]]
  output[2] = dictionary[values["max_name"]]

  return output

# -----------------------------------------------------------
def _calculate_frontiers(clusters):
  """Calculates the frontiers between the clusters

  Returns two float values specifying these frontiers
  """
  frontier_1 = (min(clusters[1]) + max(clusters[0])) / 2
  frontier_2 = (min(clusters[2]) + max(clusters[1])) / 2

  return frontier_1, frontier_2

def plot_clustering(clusters_received, 
                    title,
                    legend_word,
                    output_png,
                    plot=False):
  """Plots the result of a clustering technique like K-Means.

  Expects clusters with K = 3 groups

  Can receive:
  - A dictionary with the clusters
  - A dictionary with with the legend
  - An array with the 
  """

  fig = plt.figure()

  # Get the clusters in order
  clusters = _sort_cluster_dict(clusters_received)

  # clusters + frontiers to plot (will be used later)
  handles = ()

  # Prepare y vector to plot
  plt_y = []

  for k in clusters:
    # print(f"Cluster {k} has {len(clusters[k])} elements: {clusters[k]}")
    plt_y.append( np.zeros(len(clusters[k])) )

  # Prepare drawing options for y
  colors = ['b', 'g', 'r']
  id_color = 0
  marker = 'x'

  plt_clusters = {}
  clusters_vals = []
  for k in clusters:
    plt_clusters[k] = plt.scatter(clusters[k], plt_y[k], c=colors[id_color], marker=marker)
    id_color += 1

    # Put them into a list for the frontiers calculation
    clusters_vals.append(clusters[k])

    # Add also to the tuple for the legend function
    handles += (plt_clusters[k],)

  # Put the boundaries of each cluster
  plt_frontier = {}
  frontier_1, frontier_2 = _calculate_frontiers([clusters_vals[0], 
                                                 clusters_vals[1], 
                                                 clusters_vals[2]])
  plt_frontier["0"] = ( plt.axvline(x=frontier_1, c='r', ls='-.') )
  plt_frontier["1"] = ( plt.axvline(x=frontier_2, c='c', ls='--') )

  for k in plt_frontier:
    handles += (plt_frontier[k],)

  # Put the legend
  plt.legend(handles,
             (f"Low {legend_word}", 
              f"Medium {legend_word}", 
              f"High {legend_word}", 
              f"Frontier 1 - {frontier_1}", 
              f"Frontier 2 - {frontier_2}"))

  # Put the title
  plt.title(title)

  # Apply grid and x wide
  # plt.xlim(0, 1)
  plt.grid()
  # Show it
  if plot:
    plt.show()
  
  if os.path.isfile(output_png):
    os.remove(output_png)

  fig.savefig(output_png)

  return [frontier_1, frontier_2]

# ----------------RESULTS SECTION ----------------

# -----------------------------------------------------------
def _draw_data_in_bar(values, labels, title):
  """Draws as a bar char the specified values and tags it with the 
  specified labels and title
  """

  x = np.arange(1, len(values)+1)

  # Draw it
  plt.bar(x, values)
  # Put the labels
  plt.xticks(x, labels, rotation='vertical')
  # Put the title
  plt.title(title)
  # Show it
  plt.show()

# -----------------------------------------------------------
def draw_aggr(df, grp_col, data_col):
  """Draws the specified agreggated data column from a pandas.datataframe
  grouped by the specified aggregation column   
  """

  grouped_data = df.groupby(by=grp_col).sum()

  values = grouped_data[data_col].to_numpy(dtype=int)
  labels = grouped_data.index.to_numpy(dtype=str)

  title = data_col + " Cases"

  _draw_data_in_bar(values, labels, title)

# -----------------------------------------------------------
def draw_comparison(df, actual_col, pred_col, 
                    title="Comparison",
                    output_png="./results/test.png",
                    plot=False,
                    figsize=(6.4, 4.8)):
  """Draws to compare the actual data vs the predicted data.
  """

  g_truth = df[actual_col].to_numpy(dtype=int)
  predict = df[pred_col].to_numpy(dtype=int)

  x = np.arange(0, len(g_truth))

  # Draw it

  plt.rcParams['legend.numpoints'] = 1
  fig, ax = plt.subplots(figsize=figsize, dpi=300)

  for i in range(len(g_truth)):
    ax.plot([i,i],[predict[i], g_truth[i]], c="k", linewidth=0.5)

  ax.scatter(x, g_truth, color="green", marker="o", label="Ground Truth")
  ax.scatter(x, predict, color="red", marker="^", label="Prediction")

  # Put the labels
  # plt.xticks(x, labels, rotation='vertical')

  plt.legend()
  plt.title(title)
  plt.grid()
  
  if os.path.isfile(output_png):
    os.remove(output_png)

  fig.savefig(output_png)

  if plot:
    plt.show()

# -----------------------------------------------------------
def draw_loss(loss, val_loss, 
              title="Loss Comparison",
              output_png="./results/loss_comparison.png",
              plot=False,
              figsize=(6.4, 4.8)):
  """Draws to compare the loss
  """

  fig = plt.figure(figsize=figsize, dpi=100)

  x = np.arange(0, len(loss))

  plt.plot(x, loss, color="green", marker="o", label="Loss")
  plt.plot(x, val_loss, color="red", marker="^", label="Val Loss")

  # Put the labels
  # plt.xticks(x, labels, rotation='vertical')

  plt.legend()
  plt.title(title)
  plt.grid()
  
  if os.path.isfile(output_png):
    os.remove(output_png)

  fig.savefig(output_png)

  if plot:
    # plt.ylim(0, 0.00002)
    plt.show()

  plt.close(fig)