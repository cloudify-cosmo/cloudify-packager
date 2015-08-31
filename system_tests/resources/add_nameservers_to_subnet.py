import sys
import yaml
print(sys.argv)
filename = sys.argv[1]
with open(filename, 'r') as f:
    r = yaml.load(f.read())
props = r['node_templates']['management_subnet']['properties']
props['subnet']['dns_nameservers'] = ['8.8.4.4', '8.8.8.8']
output = yaml.dump(r)
with open(filename, 'w') as f:
    f.write(output)
print('Added DNS name servers to manager blueprint!')
