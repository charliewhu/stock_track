import streamlit as st
import httpx


class APIConnector:
    def __init__(self, base_url: str = "http://api:8000") -> None:
        self._base_url = base_url

    def get(_self, endpoint: str):
        response = httpx.get(url=f"{_self._base_url}{endpoint}")
        # TODO: error handling
        return response.json()

    @st.cache_data
    def post(_self, endpoint: str, data: dict):
        response = httpx.post(
            url=f"{_self._base_url}{endpoint}",
            json=data,
        )
        # TODO: error handling
        return response.json()

    def put(_self, data: dict):
        id = data["id"]
        response = httpx.put(
            url=f"{_self._base_url}/{id}",
            json=data,
        )
        # TODO: error handling
        return response.json()
