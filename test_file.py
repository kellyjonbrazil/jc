import jc

data_sget_headphones = """Simple mixer control 'Headphone',0
  Capabilities: pvolume pswitch
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 87
  Mono:
  Front Left: Playback 0 [0%] [-65.25dB] [off]
  Front Right: Playback 0 [0%] [-65.25dB] [off]"""

output_data_sget_headphones = jc.parse("amixer", data_sget_headphones)
print(output_data_sget_headphones)