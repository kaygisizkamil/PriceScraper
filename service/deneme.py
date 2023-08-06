import device_name_utils

device_name = "MSI PULSE 17 B13VFK-404TR Intel Core i7 13700H 32GB 1TB SSD RTX4060 Windows 11 Home 17.3"
parser = device_name_utils.DeviceNameParser(device_name)

print(parser.manufacturer) # MSI
print(parser.model) # PULSE 17 B13VFK-404TR
print(parser.processor) # Intel Core i7 13700H
print(parser.ram) # 32GB
print(parser.storage) # 1TB SSD
print(parser.os) # Windows 11 Home
print(parser.screen) # 17.3