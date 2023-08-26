import contextlib

import gradio as gr
from modules import scripts, script_callbacks, shared
import json
import os

stylespath = ""
valid_style_names = []


def get_json_content(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"A Problem occurred: {str(e)}")


def read_sdxl_styles(json_data):
    # Check that data is a list
    if not isinstance(json_data, list):
        print("Error: input data must be a list")
        return None

    names = []

    # Iterate over each item in the data list
    for item in json_data:
        # Check that the item is a dictionary
        if isinstance(item, dict):
            # Check that 'name' is a key in the dictionary
            if 'name' in item:
                # Append the value of 'name' to the names list
                names.append(item['name'])

    return names


def getStyles():
    global stylespath
    global valid_style_names
    json_path = os.path.join(scripts.basedir(), 'sdxl_styles.json')
    stylespath = json_path
    json_data = get_json_content(json_path)
    styles = read_sdxl_styles(json_data)
    valid_style_names = styles
    return styles


def createPositive(style, positive):
    json_data = get_json_content(stylespath)
    try:
        # Check if json_data is a list
        if not isinstance(json_data, list):
            raise ValueError(
                "Invalid JSON data. Expected a list of templates.")

        for template in json_data:
            # Check if template contains 'name' and 'prompt' fields
            if 'name' not in template or 'prompt' not in template:
                raise ValueError(
                    "Invalid template. Missing 'name' or 'prompt' field.")

            # Replace {prompt} in the matching template
            if template['name'] == style:
                positive = template['prompt'].replace(
                    '{prompt}', positive)

                return positive

        # If function hasn't returned yet, no matching template was found
        raise ValueError(f"No template found with name '{style}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def createNegative(style, negative):
    json_data = get_json_content(stylespath)
    try:
        # Check if json_data is a list
        if not isinstance(json_data, list):
            raise ValueError(
                "Invalid JSON data. Expected a list of templates.")

        for template in json_data:
            # Check if template contains 'name' and 'prompt' fields
            if 'name' not in template or 'prompt' not in template:
                raise ValueError(
                    "Invalid template. Missing 'name' or 'prompt' field.")

            # Replace {prompt} in the matching template
            if template['name'] == style:
                json_negative_prompt = template.get('negative_prompt', "")
                if negative:
                    negative = f"{json_negative_prompt}, {negative}" if json_negative_prompt else negative
                else:
                    negative = json_negative_prompt

                return negative

        # If function hasn't returned yet, no matching template was found
        raise ValueError(f"No template found with name '{style}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def getPrompts(style):
    return f"Positive: {createPositive(style,'{prompt}')}\nNegative: {createNegative(style,None)}"


class StyleSelectorXL(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    styleNames = getStyles()

    def title(self):
        return "Style Selector"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Style Selector", open=False):
                is_enabled = gr.Checkbox(
                    value=True, label="Enable Style Selector")
                style = gr.Dropdown(
                    label='Select Preset', choices=self.styleNames, value='base')
                pAd = gr.Textbox( label="Prompt Additions", interactive=False, value="Positive: \{prompt\}\nNegative: ")
                style.change(getPrompts, style, pAd)

        # Ignore the error if the attribute is not present

        return [is_enabled,  style]

    def process(self, p, is_enabled,  style):
        if not is_enabled:
            return

        p.extra_generation_params["Style Selector Enabled"] = True
        style = getattr(p, 'styleselector_style', style)

        for i, prompt in enumerate(p.all_prompts):      # for each image in batch

            positivePrompt = createPositive(style, prompt)
            p.all_prompts[i] = positivePrompt
        # for each image in batch
        for i, prompt in enumerate(p.all_negative_prompts):

            negativePrompt = createNegative(style, prompt)
            p.all_negative_prompts[i] = negativePrompt

    def after_component(self, component, **kwargs):
        # https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/7456#issuecomment-1414465888 helpfull link
        # Find the text2img textbox component
        if kwargs.get("elem_id") == "txt2img_prompt":  # positive prompt textbox
            self.boxx = component
        # Find the img2img textbox component
        if kwargs.get("elem_id") == "img2img_prompt":  # positive prompt textbox
            self.boxxIMG = component

def make_axis_options():
    xyz_grid = [x for x in scripts.scripts_data if x.script_class.__module__ == "xyz_grid.py"][0].module
    def confirm_style(p, xs):
        for x in xs:
            if x not in valid_style_names:
                raise RuntimeError(f"Unknown Style: {x}")

    extra_axis_options = [
        xyz_grid.AxisOption("[StyleSelector] Preset", str, xyz_grid.apply_field("styleselector_style"), confirm=confirm_style, choices=lambda: valid_style_names)
    ]
    if not any("[StyleSelector]" in x.label for x in xyz_grid.axis_options):
        xyz_grid.axis_options.extend(extra_axis_options)



def callbackBeforeUi():
    try:
        make_axis_options()
    except Exception as e:
        traceback.print_exc()
        print(f"Failed to add support for X/Y/Z Plot Script because: {e}")

script_callbacks.on_before_ui(callbackBeforeUi)
