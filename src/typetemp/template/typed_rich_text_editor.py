from dataclasses import dataclass
from typing import List

from typetemp.template.typed_template import TypedTemplate


@dataclass
class RichTextTemplate(TypedTemplate):
    feature_name: str = ""
    source = """
    import React, { useState } from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill CSS
import axios from "axios";

const App: React.FC = () => {
  const [{{ feature_name }}Title, set{{ feature_name }}Title] = useState("");
  const [editorContent, setEditorContent] = useState("");
  const [{{ feature_name }}Info, set{{ feature_name }}Info] = useState<any>(null);
  const [loading, setLoading] = useState(false);

    """


if __name__ == "__main__":
    temp = RichTextTemplate(feature_name="Vandita's Cool Feature")

    print(temp())
