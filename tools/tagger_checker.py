import pandas as pd
import streamlit as st

from ja_timex.tagger.abstime_tagger import AbstimeTagger
from ja_timex.tagger.duration_tagger import DurationTagger
from ja_timex.tagger.reltime_tagger import ReltimeTagger
from ja_timex.tagger.set_tagger import SetTagger

selected_tagger_name = st.sidebar.selectbox("Select Tagger", ("abstime", "reltime", "duration", "set"))
text = st.text_area("Text to analyze", "")


if selected_tagger_name == "abstime":
    tagger = AbstimeTagger()
elif selected_tagger_name == "reltime":
    tagger = ReltimeTagger()
elif selected_tagger_name == "duration":
    tagger = DurationTagger()
elif selected_tagger_name == "set":
    tagger = SetTagger()


if text:
    text = text.replace("\n", "").strip()
    timex = tagger.parse(text)

    if timex is None:
        st.write("No Result")
    else:
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
                timex.span,
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
                "@span",
            ],
            columns=["value"],
        )
        st.table(timex_df)
