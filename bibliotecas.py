import streamlit as st
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

try:
    import plotly.express as px
except Exception:
    px = None