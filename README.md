# PhDs Awarded in The US in 2017 Dashboard

The National Center for Science and Engineering Statistics (NCSES) of the National Science Foundation (NSF) is a statistical agency that specializes in the collection and analysis of data related to science and engineering. NCSES designs and administrates national surveys to support researches that uses its data. One of these datasets is the [Science & Engineering Doctorates](https://ncses.nsf.gov/pubs/nsf19301/data), which is a collection of tables that entails the demographic characteristics, educational history, sources of financial support, and post graduation plans of doctorate recipients. This repository contains a Plotly Dash dashboard script that aim to provide an interactive visualization on the 'popularity' of different disciplines across different states.


This dashboard contains 3 components:
- an array of radioitems
- a choropleth map
- a barplot

Select one of the three options in radioitems to choose a field (Science vs. Engineering vs. Total). The choropleth map should update accordingly. 

Hover the cursor over a state to change the barplot. The barplot contains the distribution of the count of doctorates granted in each sub-field for a given state.

This workflow is illustrated in the gif below:

![fig1](./resources/demo.gif)


## Blog Post

In addition, I have a Medium blog post that describe my dashboard. 

Topic | Post
-------|-----
Dashboard Creation | [PhDs Awarded in the US in 2017](https://michaeltang101.medium.com/phds-awarded-in-the-us-in-2017-f327fd0f1771)
