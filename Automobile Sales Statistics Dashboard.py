
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Loads the automobile sales data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options ('Yearly Statistics', 'Recession Period Statistics')
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years from 1980 to 2023 to be used in a dropdown menu.
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # Title of the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 24
            }),
    # Add two dropdown menus
    # Select Statistics Dropdown
    html.Div([
        html.Label(
            "Select Statistics:",
            style={
                'marginRight': '10px',
                'fontSize': '18px',
                'fontWeight': 'bold',
                'alignSelf': 'center'
            }
    ),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            # A dictionary that controls the appearance and layout of the dropdown element itself
            style={
                'width': '300px',
                'padding': '3px',
                'fontSize': 16,
                
            }
        )
    ],style={
        'display': 'flex',                # Use flexbox to align items side-by-side
        'flexDirection': 'row',           # Arrange items in a horizontal row
        'alignItems': 'center',           # Vertically align items to the center of the row
        'justifyContent': 'center',
        'marginBottom':'20px'
        }
    ),
    # Select Year Dropdown
    html.Div(
        id='year-dropdown-container',
        children=[
            # Label for "Select Year"
            html.Label(
                "Select Year:",
                style={
                    'marginRight': '10px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'alignSelf': 'center'
                }
            ),  
            dcc.Dropdown(
                id='select-year',
                # Generate dropdown options from year_list: each option has 'label' (visible year) and 'value' (selected year)
                # Dictionary Creation for Each Year(1980 to 2023): {'label': 1980, 'value': 1980}
                options=[{'label': i, 'value': i} for i in year_list],
                placeholder='Select-year',
                value = 1980,
                style={
                    'width': '300px',
                    'padding': '3px',
                    'fontSize': 16,
                    
                }
            )
        ],
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'center',
                'marginBottom': '20px'
            }
    ),
    html.Div([
        # Add a division for output display (graphs, chart) 
        html.Div(id='output-container', 
        className='chart-grid', 
        style={'display': 'flex',
               'flexWrap': 'wrap',
               'justifyContent': 'center'
               }),
    ])
])
# Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='year-dropdown-container', component_property='style'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    # Enable or disable the 'select-year' dropdown based on 'dropdown-statistics' selection
    # Enables(False) or Disables(True)
    if selected_statistics =='Yearly Statistics': 
        return {
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'center',
            'justifyContent': 'center',
            'marginBottom': '20px'
        }
    else: 
        return {'display': 'none'}

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
    Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics, input_year):
    # Update the output container with appropriate graphs based on selected statistics type and year.
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
# Create and display graphs for Recession Report Statistics

# Plot 1 Line Chart- Average Automobile sales over Recession Period
        # Grouping the data by the columns 'Year' and 'Automobile_Sales'
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

# Plot 2  Bar Chart- Average number of vehicles sold by vehicle type during recession        
        # Grouping the data by the columns 'Vehicle_Type' and 'Automobile_Sales' columns
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                 
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Number of Vehicles Sold by Vehicle Type during Recession Period"))
        
# Plot 3 Pie chart- Total expenditure share by vehicle type during recession
	    # Grouping the data by the columns 'Vehicle_Type' and 'Advertising_Expenditure' columns
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title="total expenditure share by vehicle type during recessions"))

# Plot 4 bar chart- Effect of unemployment rate on vehicle type and sales
        # Grouping the data by the columns 'unemployment_rate','Vehicle_Type' and 'Automobile_Sales' columns
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data,
        x='Vehicle_Type',
        y='Automobile_Sales',
        color='unemployment_rate',
        labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
        title='Effect of Unemployment Rate on Vehicle Type and Sales'))


        return [
             html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
            ]

# Create and display graphs for Yearly Report Statistics

    # Check for Yearly Statistics.                             
    elif (input_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
                              

# Yearly Statistic Report Plots                              
# Plot 1 Line Chart- Yearly Automobile sales for the whole period.
        # Grouping the data by the columns 'Year' and 'Automobile_Sales'.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, 
        x='Year',
        y='Automobile_Sales',
        title="Yearly Automobile sales"))
            
# Plot 2 Line Chart- Total Monthly Automobile sales for the selected year
	    # Grouping the data by the columns 'Month' and 'Automobile_Sales'
        monthly_auto_sales=yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(monthly_auto_sales,
            x='Month',
            y='Automobile_Sales',
            title=f'Total Monthly Automobile Sales in {input_year}'))

  # Plot 3 bar chart- Average Vehicles Sold by Vehicle Type in the Selected Year
        # Grouping the data by the columns 'Year' and 'Automobile_Sales'
        average_vehicle_type_sales=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph( figure=px.bar(average_vehicle_type_sales,
        x='Vehicle_Type',
        y='Automobile_Sales',
        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

    # Plot 4 Pie Chart- Total Advertisement Expenditure for each vehicle in the selected year
        # Grouping the data by the columns 'Vehicle_Type' and 'Advertising_Expenditure'
        total_ad_exp_type=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(total_ad_exp_type, 
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertisment Expenditure for Each Vehicle'))

# Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display':'flex'})
        ]       
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

