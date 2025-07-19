import streamlit as st

import pandas as pd
import numpy as np
import altair as alt

# Importing data
data = [
  {
    "Bacteria": "Aerobacter aerogenes",
    "Penicillin": 870,
    "Streptomycin": 1,
    "Neomycin": 1.6,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Bacillus anthracis",
    "Penicillin": 0.001,
    "Streptomycin": 0.01,
    "Neomycin": 0.007,
    "Gram_Staining": "positive",
    "Genus": "other"
  },
  {
    "Bacteria": "Brucella abortus",
    "Penicillin": 1,
    "Streptomycin": 2,
    "Neomycin": 0.02,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Diplococcus pneumoniae",
    "Penicillin": 0.005,
    "Streptomycin": 11,
    "Neomycin": 10,
    "Gram_Staining": "positive",
    "Genus": "other"
  },
  {
    "Bacteria": "Escherichia coli",
    "Penicillin": 100,
    "Streptomycin": 0.4,
    "Neomycin": 0.1,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Klebsiella pneumoniae",
    "Penicillin": 850,
    "Streptomycin": 1.2,
    "Neomycin": 1,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Mycobacterium tuberculosis",
    "Penicillin": 800,
    "Streptomycin": 5,
    "Neomycin": 2,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Proteus vulgaris",
    "Penicillin": 3,
    "Streptomycin": 0.1,
    "Neomycin": 0.1,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Pseudomonas aeruginosa",
    "Penicillin": 850,
    "Streptomycin": 2,
    "Neomycin": 0.4,
    "Gram_Staining": "negative",
    "Genus": "other"
  },
  {
    "Bacteria": "Salmonella (Eberthella) typhosa",
    "Penicillin": 1,
    "Streptomycin": 0.4,
    "Neomycin": 0.008,
    "Gram_Staining": "negative",
    "Genus": "Salmonella"
  },
  {
    "Bacteria": "Salmonella schottmuelleri",
    "Penicillin": 10,
    "Streptomycin": 0.8,
    "Neomycin": 0.09,
    "Gram_Staining": "negative",
    "Genus": "Salmonella"
  },
  {
    "Bacteria": "Staphylococcus albus",
    "Penicillin": 0.007,
    "Streptomycin": 0.1,
    "Neomycin": 0.001,
    "Gram_Staining": "positive",
    "Genus": "Staphylococcus"
  },
  {
    "Bacteria": "Staphylococcus aureus",
    "Penicillin": 0.03,
    "Streptomycin": 0.03,
    "Neomycin": 0.001,
    "Gram_Staining": "positive",
    "Genus": "Staphylococcus"
  },
  {
    "Bacteria": "Streptococcus fecalis",
    "Penicillin": 1,
    "Streptomycin": 1,
    "Neomycin": 0.1,
    "Gram_Staining": "positive",
    "Genus": "Streptococcus"
  },
  {
    "Bacteria": "Streptococcus hemolyticus",
    "Penicillin": 0.001,
    "Streptomycin": 14,
    "Neomycin": 10,
    "Gram_Staining": "positive",
    "Genus": "Streptococcus"
  },
  {
    "Bacteria": "Streptococcus viridans",
    "Penicillin": 0.005,
    "Streptomycin": 10,
    "Neomycin": 40,
    "Gram_Staining": "positive",
    "Genus": "Streptococcus"
  }
]

# Creating a daraframe
df = pd.DataFrame(data)

# Adding index
df['index'] = df.index

# Adding suffix to make into long format
df = df.rename(columns={'Penicillin':'a_Penicillin','Streptomycin':'a_Streptomycin','Neomycin':'a_Neomycin'})

# Converting to long
df_long = pd.wide_to_long(df, stubnames='a', i='index', j='Antibiotic', sep='_', suffix='.+').reset_index()

df_long.drop(columns='index',inplace=True)

df_long = df_long.rename(columns={'a':'Minimum Inhibitory Concentration (MIC)'})

# Transforming MIC
df_long['log(Minimum Inhibitory Concentration (MIC))'] = np.log(df_long['Minimum Inhibitory Concentration (MIC)'])


# Data for each Genus
pos_df = df_long[df_long['Gram_Staining'] == 'positive']
neg_df = df_long[df_long['Gram_Staining'] == 'negative']

# Adding active title
st.title("Antibiotic Effectiveness in Bacteria")
# adding subtitle
st.subheader("Penicillin works best with :green[positive] *Gram Staining bacteria, while Neomycin are more effective against :orange[negative] Gram Staining bacteria.")

# Define a shared color scale
color_scale = alt.Scale(domain=['negative','positive', ], range=["#ff9f0eff","#1fb47b"])


# Creating boxplot before faceting 
boxplot = alt.Chart(df_long).mark_boxplot().encode(
    x=alt.X("Antibiotic:N"),
    y=alt.Y('log(Minimum Inhibitory Concentration (MIC))', title='**log(Minimum Inhibitory Concentration (MIC))'),
    color=alt.Color('Gram_Staining:N', scale=color_scale),
    column=alt.Column('Gram_Staining:N', title='Gram Staining')
).properties(width=300)



# # Creating annotations for boxplot
# # creating dataframe for annotations
# annotations = [
#     ('negative','Penicillin', np.median(df_long[(df_long['Gram_Staining'] == 'negative') & (df_long['Antibiotic'] == 'Penicillin')]['log(Minimum Inhibitory Concentration (MIC))']), '⬅', 'Penicillin has a substantially lower log(MIC), indicating higer effectiness than other antibiotics'),
#     ('positive','Neomycin', np.median(df_long[(df_long['Gram_Staining'] == 'positive') & (df_long['Antibiotic'] == 'Neomycin')]['log(Minimum Inhibitory Concentration (MIC))']), '⬅', 'Neomycin has a substantially lower log(MIC), indicating higer effectiness than other antibiotics'),
# ]
# # Creating a DataFrame for annotations
# annotations_df = pd.DataFrame(annotations, columns=['Gram_Staining', 'Antibiotic', 'log(Minimum Inhibitory Concentration (MIC))', 'annotation_icon', 'annotation_text'])

# # Merge annotation data back into df_long
# df_long_annotated = df_long.merge(
#     annotations_df,
#     on=["Gram_Staining", "Antibiotic"],
#     how="left"  # Keep all rows, add annotation where available
# )

# # Mark whether annotation exists
# df_long_annotated["has_annotation"] = df_long_annotated["annotation_icon"].notna()

# base = alt.Chart(df_long_annotated).encode(
#     x="Antibiotic:N",
#     y="log(Minimum Inhibitory Concentration (MIC)):Q",
#     color=alt.Color("Gram_Staining:N", scale=color_scale)
# )

# boxplot = base.mark_boxplot().properties(width=300)

# # Annotation Layer: Only show text where annotation exists
# annotations = base.mark_text(
#     size=14, dx=-10, dy=-5, align='left'
# ).encode(
#     text=alt.condition("datum.has_annotation", "annotation_icon:N", alt.value("")),
#     tooltip="annotation_text:N"
# )

# # Layer first, then facet
# layered = alt.layer(boxplot, annotations).facet(
#     column=alt.Column("Gram_Staining:N", title="Gram Staining")
# )

# st.altair_chart(layered)


# # Creating a DataFrame for annotations

# annotation_layer = alt.Chart(annotations_df).mark_text(
#     size=14, dx=-10, dy=-5, align='left'
# ).encode(
#     x="Antibiotic:N",
#     y="log(Minimum Inhibitory Concentration (MIC)):Q",
#     text="annotation_icon",
#     tooltip="annotation_text",
#     color=alt.Color("Gram_Staining:N", scale=color_scale)
# )

# # Combining the boxplot with annotations
# boxplot = boxplot_base + annotation_layer

# # adding faceting to the boxplot
# boxplot = boxplot.facet(
#     column=alt.Column('Gram_Staining:N', title='Gram Staining'))

st.altair_chart(boxplot)

# Adding captions
st.caption("*Gram staining is a procedure performed to classify bacteria based on their cell wall characteristics")
st.caption("**MIC is the lowest concentration of a chemical that prevents visible in vitro growth of bacteria. Lower values imply higher antibiotic effectiveness")


# adding subtitle
st.header("How do the aggregated results fare for each Genus?")
st.subheader("_Penicillin_ is most effective against :green[positive] Gram Staining Streptococcus and other genera.")

pos_boxplot = alt.Chart(pos_df).mark_boxplot().encode(
    x=alt.X("Antibiotic:N"),
    y=alt.Y('log(Minimum Inhibitory Concentration (MIC))', title= "log(Minimum Inhibitory Concentration (MIC))"),
    color=alt.Color('Gram_Staining:N', scale=color_scale),
    column=alt.Column('Genus:N')
).properties(width=300)

# Creating boxplots for each Genus
st.altair_chart(pos_boxplot)


st.subheader("_Neomycin_ is effective against :orange[negative] Gram Staining bacteria across all genera")
neg_boxplot = alt.Chart(neg_df).mark_boxplot().encode(
    x=alt.X("Antibiotic:N"),
    y=alt.Y('log(Minimum Inhibitory Concentration (MIC))'),
    color=alt.Color('Gram_Staining:N', scale=color_scale),
    column=alt.Column('Genus:N', title='Genus')
).properties(width=300)

st.altair_chart(neg_boxplot)



