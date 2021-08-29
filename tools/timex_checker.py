import pandas as pd
import pendulum
import streamlit as st

from ja_timex.timex import TimexParser


def export_as_tagged_text(timexes, text):
    for timex in sorted(timexes, key=lambda x: x.span[0], reverse=True):
        # streamlit上で分かりやすいように、タグの前後を改行する
        text = text[: timex.span[0]] + "\n" + timex.to_tag() + "\n" + text[timex.span[1] :]
    return text


st.header("ja_timex Checker")
text = st.text_area("Text to parse", "")

use_reference = st.sidebar.checkbox("Use reference")
if use_reference:
    reference_year = st.sidebar.number_input("year", min_value=1, value=2021)
    reference_month = st.sidebar.number_input("month", min_value=1, max_value=12, value=7)
    reference_day = st.sidebar.number_input("day", min_value=1, max_value=31, value=18)
    reference_hour = st.sidebar.number_input("hour", min_value=0, max_value=30, value=10)
    reference_minute = st.sidebar.number_input("minute", min_value=0, max_value=60, value=00)
    reference_second = st.sidebar.number_input("second", min_value=0, max_value=60, value=00)

if use_reference:
    reference_datetime = pendulum.datetime(
        year=reference_year,
        month=reference_month,
        day=reference_day,
        hour=reference_hour,
        minute=reference_minute,
        second=reference_second,
        tz="Asia/Tokyo",
    )
    timex_parser = TimexParser(reference=reference_datetime)
    st.sidebar.write(reference_datetime)
else:
    timex_parser = TimexParser()

if text:
    text = text.replace("\n", "").strip()
    timexes = timex_parser.parse(text)

    if timexes is None:
        st.write("No Result")
    else:
        st.code(export_as_tagged_text(timexes, timex_parser.processed_text), language="xml")

        for timex in timexes:
            timex_df = pd.DataFrame(
                [
                    timex.tid,
                    timex.type,
                    timex.value,
                    timex.text,
                    timex.freq,
                    timex.quant,
                    timex.mod,
                    timex.parsed,
                    timex.span,
                    timex.pattern,
                ],
                index=["@tid", "@type", "@value", "@text", "@freq", "@quant", "@mod", "parsed", "span", "pattern"],
                columns=["value"],
            )
            st.subheader(f"{timex.tid}: {timex.text}")
            st.table(timex_df)

            st.subheader("to_datetime")
            st.write(timex.to_datetime())
            st.subheader("to_duration")
            st.write(timex.to_duration())
