import argparse
import yaml


def read_proxies(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    proxies = []
    proxy_names = []

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('socks5://'):
            parts = line.split('@')
            auth, address = parts[0].split('//')[1], parts[1]
            username, password = auth.split(':')
            server, port = address.split(':')

            proxy_name = f"Proxy{i + 1}"
            proxies.append({
                'name': proxy_name,
                'type': 'socks5',
                'server': server,
                'port': int(port),
                'username': username,
                'password': password
            })
            proxy_names.append(proxy_name)

    return proxies, proxy_names


def generate_config(proxies, proxy_names, output_file):
    config = {
        'proxies': proxies,
        'proxy-groups': [
            {
                'name': 'Auto',
                'type': 'select',
                'proxies': proxy_names
            }
        ],
        'rules': [
            'DOMAIN-SUFFIX,example.com,Auto',
            'GEOIP,CN,DIRECT',
            'MATCH,Auto'
        ]
    }

    with open(output_file, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    print(f"config.yaml 已生成在 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate Clash config.yaml from socks5 proxies list')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input socks5.txt file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output config.yaml file')

    args = parser.parse_args()

    proxies, proxy_names = read_proxies(args.input)
    generate_config(proxies, proxy_names, args.output)


if __name__ == "__main__":
    main()