import pandas as pd
import streamlit as st
import plotly.express as px
from ui import connectors

TITLE = "Production Tracker"

st.set_page_config(page_title=TITLE)


class StreamlitApp:
    def __init__(self, api: connectors.APIConnector) -> None:
        self.api = api

    def __call__(self):
        st.title(TITLE)

        # Form for adding a new row
        st.subheader("Add New Production")
        with st.form("new_production_form", clear_on_submit=True):
            date = st.date_input("Date")
            quantity = st.number_input("Quantity", min_value=0)
            submit_button = st.form_submit_button("Add New")

            if submit_button:
                # make post request
                data = {"date": str(date), "quantity": quantity}
                self.api.post("/", data)

        st.subheader("Productions")
        st.write("Edit in cells")
        df = pd.DataFrame(self.api.get("/")).sort_values("date")

        # Editable table
        edited_df = st.data_editor(
            df,
            key="data_editor",
            on_change=lambda: None,
            column_order=["id", "date", "quantity"],
        )

        # Check if any row has been edited
        edited_rows = st.session_state["data_editor"]["edited_rows"]
        if edited_rows:
            for index, edits in edited_rows.items():
                if edits:  # If there are edits for this row
                    # Create a copy of the row with updates
                    updated_row = edited_df.iloc[index].copy()

                    # Convert the updated row to a dictionary
                    row_dict = updated_row.to_dict()

                    # Post the data to the API
                    self.api.put(row_dict)
                    st.rerun()

        # Graph of productions

        # Ensure 'date' is in datetime format
        df["date"] = pd.to_datetime(df["date"])

        # Group by month and sum the quantities
        df["month"] = df["date"].dt.to_period("M").astype(str)
        monthly_data = df.groupby("month")["quantity"].sum().reset_index()

        # Generate a complete list of months from the start to the end of the date range
        start_date = df["date"].min().to_period("M").to_timestamp()
        end_date = df["date"].max().to_period("M").to_timestamp()
        all_months = pd.date_range(
            start=start_date,
            end=end_date,
            freq="MS",
        ).strftime("%Y-%m")
        all_months_df = pd.DataFrame(all_months, columns=["month"])

        # Merge the actual data with the complete list of months to ensure every month is represented
        monthly_data_complete = pd.merge(
            all_months_df, monthly_data, on="month", how="left"
        ).fillna(0)

        # Create chart
        fig = px.bar(
            monthly_data_complete,
            x="month",
            y="quantity",
            labels={"month": "Month", "quantity": "Total Quantity"},
            title="Total Quantity by Month",
        )

        # Update x-axis to show only one tick per bar
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=monthly_data_complete["month"],
                tickformat="%Y-%m",
            ),
            xaxis_title=None,  # Remove the x-axis label
            yaxis_title="fuck off",  # Remove the y-axis label
        )

        st.plotly_chart(fig)


def main():
    api = connectors.APIConnector()
    app = StreamlitApp(api=api)
    app()


if __name__ == "__main__":
    main()
