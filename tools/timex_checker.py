import pandas as pd
import streamlit as st

from ja_timex.timex import TimexParser

text = st.text_area("Text to analyze", "")


timex_parser = TimexParser()


if text:
    text = text.replace("\n", "").strip()
    timexes = timex_parser.parse(text)

    if timexes is None:
        st.write("No Result")
    else:
        for timex in timexes:
            timex_df = pd.DataFrame(
                [
                    timex.type,
                    timex.value,
                    timex.value_from_surface,
                    timex.temporal_function,
                    timex.freq,
                    timex.quant,
                    timex.mod,
                    timex.range_start,
                    timex.range_end,
                    timex.ordinal,
                    timex.parsed,
                    timex.value_format,
                    timex.additional_info,
                ],
                index=[
                    "@type",
                    "@value",
                    "@value_from_surface",
                    "@temporal_function",
                    "@freq",
                    "@quant",
                    "@mod",
                    "@range_start",
                    "@range_end",
                    "@ordinal",
                    "@parsed",
                    "@value_format",
                    "@additional_info",
                ],
                columns=["value"],
            )
            st.table(timex_df)
