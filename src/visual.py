
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =============================
# Numeric columns distributions 
# =============================

def viz_histogram(table: pd.DataFrame,
                  column_to_describe: str,
                  center_method: str | None = 'mean',
                  column_to_group: str | None = None,
                  density: bool = True,
                  ax = None
                  ):

  """
  Parameters
  ----------
  table : pandas.DataFrame
      DataFrame containing the data

  column_to_describe : str
      Name of the numeric column whose distribution should be plotted

  center_method : str or None, default = 'mean'
      Method used to calculate the center and spread
      Allowed values: 'mean', 'median', None

  column_to_group : str or None, default = None
      Name of the categorical column used to split the data into groups
      Use None to plot the full distribution without grouping
      Max number of unique values: 3

  density : bool, default = True
      If True, displays probability density
      If False, displays observation counts

  Returns
  -------
  matplotlib.axes.Axes
      Axes object containing the histogram
  """

  if not isinstance(table, pd.DataFrame):
    raise TypeError(f'table must be a pandas DataFrame')

  if column_to_describe not in table.columns:
      raise ValueError(f'{column_to_describe} is not a column in table')

  if table[column_to_describe].dropna().empty:
    raise ValueError(f'{column_to_describe} contains only null values')

  if not pd.api.types.is_numeric_dtype(table[column_to_describe]):
    raise ValueError(f'{column_to_describe} must be a numeric type')

  if center_method not in (None, 'mean', 'median'):
    raise ValueError(f'{center_method} can only be None, "mean" or "median"')

  if column_to_group is not None and column_to_group not in table.columns:
      raise ValueError(f'{column_to_group} is not a column in table')

  if column_to_group is not None and table[column_to_group].nunique() > 3:
    raise ValueError(f'{column_to_group} contains too many unique values. Max: 3')

  if not isinstance(density, bool):
      raise ValueError('density must be True or False')

  if ax is None:
    _, ax = plt.subplots()

  titles = []
  bin_edges = np.histogram_bin_edges(table[column_to_describe].dropna(), bins = 'auto')

  if column_to_group is None:
      values_to_group = ['Total']
      title = column_to_describe
  else:
      values_to_group = table[column_to_group].dropna().unique()
      title = f'{column_to_describe} by {column_to_group}'

  number_of_values_to_group = len(values_to_group)

  counter = 0
  while counter < number_of_values_to_group:

    if column_to_group is None:
      histogram_base = table[column_to_describe].dropna()
    else:
      histogram_base = table[table[column_to_group] == values_to_group[counter]][column_to_describe].dropna()

    histogram_base.hist(bins = bin_edges,
                        color = colors['main']['medium'][counter],
                        alpha = 0.8,
                        density = density,
                        label = values_to_group[counter],
                        ax = ax)

    subtitle_with_stats = f'{values_to_group[counter]}: size = {len(histogram_base)}'

    if center_method == 'mean':
      center = histogram_base.mean()
      stdv = histogram_base.std(ddof = 1)
      min_span = center - stdv
      max_span = center + stdv
      subtitle_with_stats = subtitle_with_stats + f' | {center_method} = {round(center, 2)}'

    elif center_method == 'median':
      center = histogram_base.median()
      min_span = np.percentile(histogram_base, 25)
      max_span = np.percentile(histogram_base, 75)
      subtitle_with_stats = subtitle_with_stats + f' | {center_method} = {round(center, 2)}'

    titles.append(subtitle_with_stats)

    if center_method is not None:
      ax.axvline(center, color = colors['main']['dark'][counter])
      ax.axvspan(min_span, max_span, color = colors['main']['light'][counter], zorder = 0)

    if column_to_group is not None:
      ax.legend()

    counter += 1

  ax.set_title(f'{title} \n' + '\n'.join(titles), size = 10)

  ax.spines['top'].set_color(colors['neutral']['medium'])
  ax.spines['right'].set_color(colors['neutral']['medium'])
  ax.spines['bottom'].set_color(colors['neutral']['medium'])
  ax.spines['left'].set_color(colors['neutral']['medium'])

  ax.grid(False)

  return ax


def viz_hbars (table,
               column_to_group,
               numeric_column,
               column_to_color = None,
               relative = False,
               ax = None):
  # check values are unique for [numeric_column].count()

  table[column_to_group] = table[column_to_group].astype('str')

  grouped_table = table.groupby(column_to_group, as_index = False)[numeric_column].count().sort_values(by = numeric_column, ascending = True)

  if column_to_color is None:
    ax.barh(grouped_table[column_to_group], grouped_table[numeric_column], color = colors['main']['medium'][0])
    
    total = grouped_table[numeric_column].sum()
    for container in ax.containers:
      labels = [
      f'{bar.get_width():.0f} | {bar.get_width() / total:.0%}'
      if relative
      else f'{bar.get_width():.0f}'
      for bar in container]

    ax.bar_label(container, labels = labels, label_type = 'center', fontsize = 9)

  else:
    n = table[column_to_color].nunique()
    if relative:
        t = pd.crosstab(
            table[column_to_group],
            table[column_to_color],
            normalize = 'index')
    else:
        t = pd.crosstab(
            table[column_to_group],
            table[column_to_color])

    ax = t.plot.barh(stacked = True, color = colors['main']['medium'][:n], ax = ax)

    for container in ax.containers:
        labels = [
            f'{bar.get_width():.0%}'
            if relative and bar.get_width() >= 0.05 else f'{bar.get_width():.0f}'
            if not relative and bar.get_width() > 0 else ''
            for bar in container
        ]
        ax.bar_label(container, labels = labels, label_type = 'center', fontsize = 9)

  if column_to_color is not None:
      ax.legend(
          loc = 'upper center',
          bbox_to_anchor = (0.5, -0.1))

  ax.spines['top'].set_color(colors['neutral']['medium'])
  ax.spines['right'].set_color(colors['neutral']['medium'])
  ax.spines['bottom'].set_color(colors['neutral']['medium'])
  ax.spines['left'].set_color(colors['neutral']['medium'])
