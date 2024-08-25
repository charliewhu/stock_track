import pandas as pd
import streamlit as st
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

        st.header("Productions")
        st.write("Edit in cells")
        df = pd.DataFrame(self.api.get("/"))

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

        # Graph of productions

        # Filter for each Field


def main():
    api = connectors.APIConnector()
    app = StreamlitApp(api=api)
    app()


if __name__ == "__main__":
    main()
