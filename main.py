import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CCC",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed")

# Excel file name
excel_file_name = "./bauteil-database.xlsx"

# Load excel file
@st.cache_resource
def load_excel(excel_file_name):
    excel_file = pd.ExcelFile(excel_file_name)
    return excel_file

# Load Bauteil data
def load_bauteil_data(excel_file):
    bt = excel_file.parse("Katalog-Uebersicht")
    bauteilName = bt["Name"].tolist()
    bauteilType = bt["Type"].tolist()
    bauteilMaterial = bt["Material"].tolist()
    return bauteilName, bauteilType, bauteilMaterial


def get_bauteil_dataframe(excel_file, bauteil_name):
    bt = excel_file.parse("Katalog-Uebersicht")
    bt = bt.loc[bt["Name"] == bauteil_name]
    return bt

### Do not need the bauteil in the function
# Load catalog data
@st.cache_data
def load_katalog_data(_excel_file, bauteil):
    bom = _excel_file.parse("BOM")

    # Initialize bomSelected with the same columns as bom
    bomSelected = pd.DataFrame(columns=bom.columns)
    if bom["Name"].str.contains(bauteil).any():
        # Get index of row where Name is equal to bauteil
        index = bom[bom["Name"] == bauteil].index.values.astype(int)[0]
        # Increase index by 1 to get the next row
        index += 1
        # While column "Material level" is equal to 1, add the row to bomSelected dataframe and increase index by 1
        while bom.loc[index,"Material level"] == 1:
            bomSelected.loc[len(bomSelected.index)] = bom.iloc[index]
            index += 1

    # Create a list for each property
    materialIdList = bomSelected["Material ID"].tolist()
    materialThickness = bomSelected["Thickness [m]"].tolist()

    ###### Database Material ######

    # Create a new empty DataFrame
    filteredMaterials = pd.DataFrame()
    # Loop through the list of material IDs and add the rows to the new DataFrame
    mat = excel_file.parse("Materials")
    for material_id in materialIdList:
        row_mat = mat[mat["Material ID"] == material_id]
        filteredMaterials = pd.concat([filteredMaterials, row_mat])

    # Create a list for each property
    materialName = filteredMaterials["Name"].tolist()
    materialMinThickness = filteredMaterials["Min thickness"].tolist()
    materialMaxThickness = filteredMaterials["Max thickness"].tolist()

    # If material name repeats, add a number to the end
    # This is necessary because the slider widget does not accept repeated names
    material_dict = {}
    count_dict = {}

    # First pass to count occurrences
    for material in materialName:
        if material in count_dict:
            count_dict[material] += 1
        else:
            count_dict[material] = 1

    # Second pass to rename
    for i in range(len(materialName)):
        material = materialName[i]
        if count_dict[material] > 1:
            if material in material_dict:
                material_dict[material] += 1
            else:
                material_dict[material] = 1
            materialName[i] = f"{material} {str(material_dict[material]).zfill(2)}"

    # Zip the lists together
    materialList = list(zip(
        materialName,
        materialMinThickness,
        materialMaxThickness,
        materialThickness
    )
    )

    return materialList


@st.cache_data
def get_properties_of_bauteil(bauteil):
    bauteil_dataframe = get_bauteil_dataframe(excel_file, bauteil)

    # Get value type from the dataframe
    # bauteilType = bauteil_dataframe["Type"].tolist()[0]
    bauteilMaterial = bauteil_dataframe["Material"].tolist()[0]
    bauteilBuildingClass = bauteil_dataframe["Building class"].tolist()[0]
    bauteilFireProofClass = bauteil_dataframe["Fire proof class"].tolist()[0]
    bauteilUValue = bauteil_dataframe["U-value"].tolist()[0]
    bauteilSoundProof1 = bauteil_dataframe["Sound proof 1"].tolist()[0]
    bauteilSoundProof2 = bauteil_dataframe["Sound proof 2"].tolist()[0]
    bauteilPreFabricated = bauteil_dataframe["Pre-fabricated"].tolist()[0]
    bauteilExposed = bauteil_dataframe["Exposed"].tolist()[0]

    # Converts the list propertiesFrame to a Pandas DataFrame
    propertiesFrame = pd.DataFrame([
        bauteil,
        bauteilMaterial,
        bauteilBuildingClass,
        bauteilFireProofClass,
        bauteilUValue,
        bauteilSoundProof1,
        bauteilSoundProof2,
        bauteilPreFabricated,
        bauteilExposed,
        "0.15", # Update with GWP
        "0.15", # Update with Embodied energy
        "0.15"  # Update with Cost
    ])
    # Rename the rows and columns
    new_row_names = [
        'Type',
        'Core material',
        'Building class',
        'Fire proof class',
        'U-value',
        'Sound proof ¹',
        'Sound proof ²',
        'Pre-fabricated',
        'Finishing',
        'GWP [kg CO₂/m²]',
        'Embodied energy [MJ/m²]',
        'Cost [€/m²]'
    ]
    propertiesFrame.rename(index=dict(enumerate(new_row_names)), inplace=True)
    propertiesFrame.rename(columns={0: "Value"}, inplace=True)
    return propertiesFrame


@st.cache_data
def get_properties_of_bauteil_list(bauteil_list):
    # For each bauteil in bauteil_list call get_properties_of_bauteil and return one dataframe
    propertiesFrame = pd.DataFrame()
    for bauteil in bauteil_list:
        propertiesFrame = pd.concat([propertiesFrame, get_properties_of_bauteil(bauteil)], axis=1)
    propertiesFrame = propertiesFrame.transpose()
    return propertiesFrame


# Load data
excel_file = load_excel(excel_file_name)
bauteilName, bauteilType, bauteilMaterial = load_bauteil_data(excel_file)

st.header('CCC - Circular Component Creator')

# image = Image.open('./logo2.png')
# st.image(image, width=400)

st.write(
    'We develop tools based on the latest Eurocode and DIN norms to help us deliver the most '
    'reliable roadmaps. The **Circular Component Creator** allow us to compare multiple construction component systems and '
    'fine-tune them to fit the design criteria, budget and sustainable goals of our clients.')



st.header('1 - Filter components library')

with st.expander("Filter", expanded=True):
    st.write('We have a selection of relevant components so you can compare them with your creation. You can use the options below to filter for the components you are interested in.')
    type_col, core_material_col = st.columns([0.2, 0.8], gap="small")

    with type_col:
        st.subheader('Type')
        cb_externalWalls = st.checkbox("External walls", value=True)
        cb_internalWalls = st.checkbox("Internal walls", value=True)
        cb_partitionWalls = st.checkbox("Partition walls", value=True)
        cb_slabs = st.checkbox("Slabs", value=True)
        cb_roofs = st.checkbox("Roofs", value=True)

    with core_material_col:
        # Sidebar Materials
        st.subheader('Core material')
        cb_massTimber = st.checkbox("Mass Timber", value=True)
        cb_panelConstruction = st.checkbox("Panel construction", value=True)
        cb_clayBrick = st.checkbox("Clay brick", value=True)
        cb_calciumSilicateBrick = st.checkbox("Calcium silicate brick", value=True)
        cb_concrete = st.checkbox("Concrete", value=True)

st.header('2 - Select your favorite components')

# Use both bauteilType and bauteilMaterial to filter the bauteilName list using the checkboxes above
bauteilList = []
for i in range(len(bauteilName)):
    if (
            (bauteilType[i] == "External walls" and cb_externalWalls) or
            (bauteilType[i] == "Internal walls" and cb_internalWalls) or
            (bauteilType[i] == "Partition walls" and cb_partitionWalls) or
            (bauteilType[i] == "Slabs" and cb_slabs) or
            (bauteilType[i] == "Roofs" and cb_roofs)
    ):
        if (
                (bauteilMaterial[i] == "Mass Timber" and cb_massTimber) or
                (bauteilMaterial[i] == "Panel construction" and cb_panelConstruction) or
                (bauteilMaterial[i] == "Clay brick" and cb_clayBrick) or
                (bauteilMaterial[i] == "Calcium silicate brick" and cb_calciumSilicateBrick) or
                (bauteilMaterial[i] == "Concrete" and cb_concrete)
        ):
            bauteilList.append(bauteilName[i])
df_data = get_properties_of_bauteil_list(bauteilList)
column_names = df_data.columns.tolist()
df_data["Selected"] = [False] * len(df_data)
df_data = df_data[["Selected"] + column_names]

edited_df = st.data_editor(
    df_data,
    column_config={
        "Selected": st.column_config.CheckboxColumn(
            "Select",
            help="Select your favorite components",
        )
    },
    use_container_width=True,
    disabled=column_names,
    hide_index=True
)

st.divider()

st.header('3 - Create your own component')
st.write('You can use the options below to configure the component.')
materialThickness = {}
materialList = load_katalog_data(excel_file, "TRD-tr-HBV-GKL45-si")

selector_col, slider_col, svg_col = st.columns([0.25, 0.20, 0.8], gap="small")

with selector_col:
    st.subheader('Material')
with slider_col:
    st.subheader('Thickness')
with svg_col:
    st.subheader('Visualisation')

# For loop through materialList
# get index of for loop
for i in range(len(materialList)):
    material = materialList[i]
    # Create a slider for each material
    with selector_col:
        option = st.selectbox(
            "Layer " + str(i + 1),
            (material[0],),
            label_visibility="visible"
            )
    with slider_col:
        custom_value = st.number_input(
            "Range: " + str(material[1]) + " - " + str(material[2]),
            min_value = material[1],
            max_value = material[2],
            value = material[3],
            key = i,
            label_visibility = "visible"
            )
with svg_col:
    st.image(
        "<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' style='fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)' /></svg>",
        width=100,
    )

st.divider()
st.header('4 - Components comparison')
st.write(
    'Here we compare the selected components from the library with your creation.'
)
# st.subheader('Your favorite components')
# get the edited_df with only the selected rows and without the selected column
selected_bauteil = edited_df[edited_df["Selected"]]
st.dataframe(selected_bauteil.drop(columns=["Selected"]), use_container_width=True, hide_index=True)

# only get elements from data_df where selected is true
selected_bauteilList = edited_df[edited_df["Selected"]]["Type"].tolist()

# Graphs
graph1_col, graph2_col = st.columns(2, gap="large")
with graph1_col:
    st.subheader('Some data')
    st.bar_chart(
        # Enter your data below! Usually this is not a dict, but a Pandas Dataframe.,
        data={'time': [0, 1, 2, 3, 4, 5, 6], 'stock_value': [100, 200, 150, 300, 450, 500, 600]},
        x='time',
        y='stock_value',
        height=460
    )

with graph2_col:
    st.subheader('More data 2')
    st.line_chart(
        # Enter your data below! Usually this is not a dict, but a Pandas Dataframe.,
        data={'time': [0, 1, 2, 3, 4, 5, 6], 'stock_value': [100, 200, 150, 300, 450, 500, 600]},
        x='time',
        y='stock_value',
        height=460
    )
