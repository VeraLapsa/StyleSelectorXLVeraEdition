## Style Selector

This repository contains a Automatic1111 Extension allows users to select and apply different styles to their inputs using a .json file to store the styles.

Also supports xyz grid script in A1111.

### Styles

Released positive and negative templates are used to generate stylized prompts. Just install extension, then the Styles panel will appear in the accordion.

### Installation

Enter this repo's URL in Automatic1111's extension tab "Install from Url":

https://github.com/VeraLapsa/StyleSelectorXLVeraEdition.git

### Usage

Enable or Disable it On Extension's panel, Write your subject into Prompt field,
Select Style then hit Generate!
The selected style will be applied to your current prompts.

If using with the xyz script:
* Enable Style Selector in the accordion.
* ```[StyleSelector] Preset``` is the axis option.
* Only use it in 1 axis.

### My TODOs when time permits

 Figure out how to enable it if the xyz script is used but isn't enabled in the accordion.

 Allow for multiple style json files with each one being able to be used in the xyz script.
### Thanks

Original repo by https://github.com/ahgsql/StyleSelectorXL.git

Huge thanks for https://github.com/twri/sdxl_prompt_styler as i got style json file's original structure from his repo.

### License

This project is licensed under the MIT License
