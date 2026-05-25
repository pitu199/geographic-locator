#!/usr/bin/env python3
"""
==========================================================================
                    Geographic Locator - v1.0
                  Author: Assam's Hacker
              For authorized penetration testing only
==========================================================================
"""

import os, sys, json, time, socket, argparse, platform, subprocess, webbrowser
from datetime import datetime

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_OK = True
except ImportError:
    COLOR_OK = False

if COLOR_OK:
    R, G, Y, C, B, M, W, X = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE, Style.RESET_ALL
else:
    R = G = Y = C = B = M = W = X = ""

BANNER = f"""
{R}╔══════════════════════════════════════════════════════════════╗
{R}║                                                              ║
{R}║  {C}█████╗ {R}██████╗ ███████╗███████╗ █████╗ ███╗   ███╗{X}  ║
{R}║  {C}██╔══██╗{R}██╔══██╗██╔════╝██╔════╝██╔══██╗████╗ ████║{X}  ║
{R}║  {C}███████║{R}██████╔╝███████╗███████╗███████║██╔████╔██║{X}  ║
{R}║  {C}██╔══██║{R}██╔══██╗╚════██║╚════██║██╔══██║██║╚██╔╝██║{X}  ║
{R}║  {C}██║  ██║{R}██████╔╝███████║███████║██║  ██║██║ ╚═╝ ██║{X}  ║
{R}║  {C}╚═╝  ╚═╝{R}╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝{X}  ║
{R}║                                                              ║
{R}║  {G}██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗{R}          ║
{R}║  {G}██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗{R}         ║
{R}║  {G}███████║███████║██║     █████╔╝ █████╗  ██████╔╝{R}         ║
{R}║  {G}██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗{R}         ║
{R}║  {G}██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║{R}         ║
{R}║  {G}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{R}         ║
{R}║                                                              ║
{R}║  {Y}══════════════════════════════════════════════════════{R}      ║
{R}║  {C}         Geographic Locator v1.0{R}                          ║
{R}║  {Y}══════════════════════════════════════════════════════{R}      ║
{R}║                                                              ║
{R}║  {W}► IP Geolocation   ► WiFi Positioning{R}                     ║
{R}║  {W}► Altitude/Elevation   ► Google Maps{R}                      ║
{R}║                                                              ║
{R}║  {M}[!] Authorized Pentesting Tool{R}                            ║
{R}║  {M}[!] For security professionals only{R}                       ║
{R}║                                                              ║
{R}╚══════════════════════════════════════════════════════════════╝{X}
"""

def log(msg, tag="+"):
    ts = datetime.now().strftime("%H:%M:%S")
    c = {"+": G, "-": R, "*": Y, "!": M}
    print(f" {c.get(tag, W)}[{ts}]{X} {c.get(tag, W)}[{tag}]{X} {msg}")

def check_deps():
    if not REQUESTS_OK:
        log("Install requests: pip install requests", "-")
        sys.exit(1)

def get_elevation(lat, lon):
    check_deps()
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            elev = r.json().get("elevation", [None])
            return round(elev[0], 2) if elev and elev[0] is not None else None
    except: pass
    return None

def geolocate_ip(target_ip=None, show_map=False):
    check_deps()
    url = f"http://ip-api.com/json/{target_ip}" if target_ip else "http://ip-api.com/json/"
    log(f"Looking up {'IP: ' + target_ip if target_ip else 'your own public IP'}...", "*")
    try:
        data = requests.get(url, timeout=10).json()
    except Exception as e:
        log(f"API request failed: {e}", "-")
        return None
    if data.get("status") != "success":
        log(f"Geolocation failed: {data.get('message', 'unknown error')}", "-")
        return None
    result = {
        "ip": data.get("query","N/A"), "country": data.get("country","N/A"),
        "country_code": data.get("countryCode","N/A"), "region": data.get("regionName","N/A"),
        "region_code": data.get("region","N/A"), "city": data.get("city","N/A"),
        "zip": data.get("zip","N/A"), "lat": data.get("lat",0), "lon": data.get("lon",0),
        "timezone": data.get("timezone","N/A"), "isp": data.get("isp","N/A"),
        "org": data.get("org","N/A"), "as": data.get("as","N/A"),
    }
    print(f"""
{C}┌─────────────────────────────────────────────────────────┐
{C}│             IP GEOLOCATION RESULTS                      │
{C}└─────────────────────────────────────────────────────────┘{X}
 {W}IP Address :{X}  {G}{result['ip']}{X}
 {W}Country    :{X}  {result['country']} ({result['country_code']})
 {W}Region     :{X}  {result['region']} ({result['region_code']})
 {W}City       :{X}  {result['city']}
 {W}Postal/ZIP :{X}  {result['zip']}
 {W}Latitude   :{X}  {Y}{result['lat']}{X}
 {W}Longitude  :{X}  {Y}{result['lon']}{X}
 {W}Timezone   :{X}  {result['timezone']}
 {W}ISP        :{X}  {result['isp']}
 {W}Org        :{X}  {result['org']}
 {W}AS         :{X}  {result['as']}
    """)
    alt = get_elevation(result["lat"], result["lon"])
    if alt:
        result["altitude_m"] = alt
        result["altitude_ft"] = round(alt * 3.28084, 2)
        print(f" {W}Altitude   :{X}  {C}{alt} meters{X} ({C}{result['altitude_ft']} feet{X})")
    maps_url = f"https://www.google.com/maps?q={result['lat']},{result['lon']}"
    print(f"\n {W}Google Maps:{X}  {B}{maps_url}{X}")
    if show_map:
        webbrowser.open(maps_url)
    return result

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        log(f"Resolved '{target}' -> {ip}", "+")
        return ip
    except socket.gaierror:
        log(f"Could not resolve '{target}'", "-")
        return None

def altitude_lookup():
    print(f"\n{Y}=== Altitude / Elevation Lookup ==={X}\n")
    try:
        lat = float(input(" Enter latitude : ").strip())
        lon = float(input(" Enter longitude: ").strip())
    except ValueError:
        log("Invalid coordinates.", "-")
        return
    elev = get_elevation(lat, lon)
    if elev is not None:
        elev_ft = round(elev * 3.28084, 2)
        print(f"\n {G}[+]{X} Elevation at ({lat}, {lon}):")
        print(f"     {C}{elev} meters{X}")
        print(f"     {C}{elev_ft} feet{X}")
        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        print(f"\n {W}Google Maps:{X} {B}{maps_url}{X}")
    else:
        log("Could not retrieve elevation data.", "-")

def scan_wifi_aps(interface=None):
    aps = []
    system = platform.system().lower()
    try:
        if system == "windows":
            result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=Bssid"], capture_output=True, text=True, timeout=15)
            current_mac = None
            for line in result.stdout.split("\n"):
                line = line.strip()
                if "BSSID" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        current_mac = ":".join(parts[1:]).strip()
                elif "Signal" in line and current_mac:
                    try:
                        sig_str = line.split(":")[1].strip().replace("%", "")
                        sig_val = int(sig_str)
                        sig_dbm = int((sig_val / 2) - 100)
                        aps.append({"macAddress": current_mac, "signalStrength": sig_dbm})
                    except: pass
                    current_mac = None
        elif system == "linux":
            iface = interface or "wlan0"
            log(f"Scanning WiFi on '{iface}'...", "*")
            result = subprocess.run(["sudo", "iwlist", iface, "scan"], capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return []
            current_mac = None
            for line in result.stdout.split("\n"):
                line = line.strip()
                if "Address:" in line and "Cell" in line:
                    parts = line.split("Address:")
                    if len(parts) > 1:
                        current_mac = parts[1].strip()
                elif "Signal level=" in line and current_mac:
                    try:
                        sig_part = line.split("Signal level=")[1].split()[0]
                        aps.append({"macAddress": current_mac, "signalStrength": int(sig_part)})
                    except: pass
                    current_mac = None
    except: pass
    return aps

def wifi_geolocate(api_key=None, interface=None):
    check_deps()
    if not api_key:
        log("No Google API key. Falling back to IP geolocation.", "!")
        return geolocate_ip()
    aps = scan_wifi_aps(interface)
    if not aps:
        log("No WiFi APs found. Falling back to IP geolocation.", "!")
        return geolocate_ip()
    log(f"Found {len(aps)} WiFi AP(s). Querying Google...", "*")
    try:
        r = requests.post(f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}", json={"considerIp": True, "wifiAccessPoints": aps}, timeout=15)
        data = r.json()
    except Exception as e:
        log(f"WiFi geolocation failed: {e}", "-")
        return geolocate_ip()
    if "location" not in data:
        return geolocate_ip()
    lat, lon = data["location"]["lat"], data["location"]["lng"]
    accuracy = data.get("accuracy", 0)
    print(f"""
{C}┌─────────────────────────────────────────────────────────┐
{C}│          WIFI GEOLOCATION RESULTS                       │
{C}└─────────────────────────────────────────────────────────┘{X}
 {W}Latitude   :{X}  {Y}{lat}{X}
 {W}Longitude  :{X}  {Y}{lon}{X}
 {W}Accuracy   :{X}  +/-{accuracy}m
    """)
    elev = get_elevation(lat, lon)
    if elev:
        print(f" {W}Altitude   :{X}  {C}{elev}m{X}")
    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
    print(f"\n {W}Google Maps:{X}  {B}{maps_url}{X}")
    return {"lat": lat, "lon": lon, "accuracy": accuracy}

def open_in_maps(lat, lon):
    webbrowser.open(f"https://www.google.com/maps?q={lat},{lon}")

def interactive_mode():
    print(BANNER)
    print(f" {C}[+] Welcome to Geographic Locator{X}\n")
    ip_data = geolocate_ip()
    if ip_data:
        log(f"IP geolocation -> ({ip_data['lat']}, {ip_data['lon']})", "+")
    print()
    use_wifi = input(f" {Y}[?]{X} Enter Google API key for WiFi, or Enter to skip: ").strip()
    if use_wifi:
        wifi_geolocate(api_key=use_wifi)
    print(f"""
{Y}======================================================{X}
{Y}                   SCAN COMPLETE                       {X}
{Y}======================================================{X}
 {W}Target IP  :{X}  {ip_data.get('ip','N/A') if ip_data else 'N/A'}
 {W}Location   :{X}  {ip_data.get('city','N/A') if ip_data else 'N/A'}, {ip_data.get('region','N/A') if ip_data else 'N/A'}
 {W}Coordinates:{X}  {Y}{ip_data.get('lat','N/A') if ip_data else 'N/A'}, {ip_data.get('lon','N/A') if ip_data else 'N/A'}{X}
 {W}Altitude   :{X}  {C}{ip_data.get('altitude_m','N/A') if ip_data else 'N/A'}m{X}
{Y}======================================================{X}
    """)
    if ip_data and input(f" {Y}[?]{X} Open in Google Maps? (y/n): ").strip().lower() == "y":
        open_in_maps(ip_data["lat"], ip_data["lon"])

def main():
    parser = argparse.ArgumentParser(
        description="Geographic Locator - IP/WiFi Geolocation & Altitude Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python geographic_locator.py -i                    Interactive mode
  python geographic_locator.py -m                    My own IP geolocation
  python geographic_locator.py -t 8.8.8.8            Lookup a target IP
  python geographic_locator.py -t example.com        Resolve domain + geolocate
  python geographic_locator.py -a 37.7749 -122.4194  Get altitude at coordinates
  python geographic_locator.py -m -g                 My IP + open in Google Maps
        """)
    parser.add_argument("-i", "--interactive", action="store_true", help="Run interactive mode")
    parser.add_argument("-m", "--myip", action="store_true", help="Geolocate your own public IP")
    parser.add_argument("-t", "--target", type=str, metavar="IP/DOMAIN", help="Target IP or domain")
    parser.add_argument("-a", "--altitude", nargs=2, metavar=("LAT", "LON"), help="Lookup altitude")
    parser.add_argument("-w", "--wifi", action="store_true", help="WiFi-based geolocation")
    parser.add_argument("-k", "--apikey", type=str, metavar="KEY", help="Google API key for WiFi")
    parser.add_argument("-g", "--google-maps", action="store_true", help="Open in Google Maps")
    parser.add_argument("-I", "--interface", type=str, metavar="IFACE", help="WiFi interface")

    args = parser.parse_args()

    if not REQUESTS_OK:
        print(f"\n {R}[-]{X} Missing: requests. Install: pip install requests\n")
        sys.exit(1)

    if len(sys.argv) == 1:
        print(BANNER)
        parser.print_help()
        print()
        return

    if args.interactive:
        interactive_mode(); return
    if args.altitude:
        print(BANNER)
        lat, lon = float(args.altitude[0]), float(args.altitude[1])
        elev = get_elevation(lat, lon)
        if elev:
            elev_ft = round(elev * 3.28084, 2)
            print(f"\n {G}[+]{X} Elevation at ({lat}, {lon}):")
            print(f"     Altitude: {C}{elev}m{X} ({C}{elev_ft}ft{X})")
            print(f"\n {W}Google Maps:{X} {B}https://www.google.com/maps?q={lat},{lon}{X}")
            if args.google_maps: webbrowser.open(f"https://www.google.com/maps?q={lat},{lon}")
        else: log("Could not retrieve elevation.", "-")
        return
    if args.wifi:
        print(BANNER)
        wifi_geolocate(api_key=args.apikey, interface=args.interface); return
    if args.target:
        print(BANNER)
        target = args.target
        ip = target
        if not target.replace(".","").isdigit():
            resolved = resolve_target(target)
            if not resolved: sys.exit(1)
            ip = resolved
        geolocate_ip(ip, show_map=args.google_maps); return
    if args.myip:
        print(BANNER)
        geolocate_ip(show_map=args.google_maps); return

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n\n {Y}[!]{X} Interrupted."); sys.exit(0)
    except Exception as e: print(f"\n {R}[-]{X} Error: {e}"); sys.exit(1)