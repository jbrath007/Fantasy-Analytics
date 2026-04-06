to create a table using matplot
first variation:
`import matplotlib.pyplot as plt`

`Variable = dataframe.sort_values("name_of_table", ascending=False).head(10)`
==`#head means number of lines to show`==
`plt.figure()`
`plt.bar(Variable["name"], variable["name_of_table"])`
`plt.xticks(rotation=45)`
`plt.title("My Graph Title")`
`plt.xlabel("X_axis name")`
`plt.ylabel("Y axis name")`

`plt.show()`

`plt.savefig("name_of_picture.png")`

Iteration 2:

`plt.figure()`

`Variable = dataframe.sort_value("fantasy_points", ascending=True).tail(10)`

`plt.barh(Variable["name"], Variable["fantasy_points"])`
`plt.title("graph title")`
`plt.xlabel("x axis label")`

`plt.tight_layout()`
`plt.savefig("name_of_picture.png")`
`plt.show()`