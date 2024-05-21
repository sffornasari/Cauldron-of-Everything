# Last modified by S.F.Fornasari [25.05.2024]
import numpy as np
import numpy.typing as npt


def TiberiEtAl2018(gmp: str, mag: float, dists: npt.ArrayLike, vs30s: npt.ArrayLike) -> npt.ArrayLike:

    """ Function to compute the GMPE by Tiberi et al. (2018).

    Args:
      - gmp: ground motion parameter to compute the GMPE for;
      - mag: magnitude of the event;
      - dists: array(-like) of epicentral distances (in km);
      - vs30s: array(-like) of Vs30 values.

    Output:
      - mean: array of mean values of the GMPE (in cm/s**2 or cm/s or cm, depending on the GMP).
    """
    # Tiberi et al. (2018) GMPE parameters     
    params = {"pgv": {"a":-1.679506, "b":0.865751, "c":-2.074698, "d":8.478378,  "sA":0.000000, "sB":0.101583, "sC":0.350503, "sD": 0.132607, "sE":0.240249, "sigmatot":0.406312},
        "pga": {"a": 1.132003, "b":0.717163, "c":-2.523451, "d":11.001275, "sA":0.000000, "sB":0.118430, "sC":0.283016, "sD":-0.024014, "sE":0.339207, "sigmatot":0.464516},
        "ia ": {"a":-3.476919, "b":1.373298, "c":-3.189469, "d":6.631724,  "sA":0.000000, "sB":0.177052, "sC":0.457079, "sD":-0.038237, "sE":0.540782, "sigmatot":0.743363},
        "ih ": {"a":-1.553305, "b":0.890095, "c":-1.874366, "d":7.496964,  "sA":0.000000, "sB":0.104991, "sC":0.367493, "sD": 0.184603, "sE":0.210600, "sigmatot":0.386165},
        "pgd": {"a":-4.487469, "b":1.092399, "c":-1.582077, "d":4.746987,  "sA":0.000000, "sB":0.107645, "sC":0.424684, "sD": 0.300167, "sE":0.093353, "sigmatot":0.393106},
        "sa0.3": {"a": 0.321608, "b":0.817793, "c":-2.188081, "d":12.245043, "sA":0.000000, "sB":0.134044, "sC":0.354773, "sD": 0.142426, "sE":0.167675, "sigmatot":0.417201},
        "sa1.0": {"a":-2.609323, "b":0.984937, "c":-1.324107, "d":4.097013,  "sA":0.000000, "sB":0.131329, "sC":0.427318, "sD": 0.550000, "sE":0.050678, "sigmatot":0.377312},
        "sa3.0": {"a":-3.924920, "b":1.061718, "c":-1.237628, "d":2.630822,  "sA":0.000000, "sB":0.074432, "sC":0.390749, "sD": 0.182565, "sE":0.045685, "sigmatot":0.368224},}

    # Get params
    gmpl = gmp.lower()
    a = params[gmpl]["a"]
    b = params[gmpl]["b"]
    c = params[gmpl]["c"]
    d = params[gmpl]["d"]
    sA = params[gmpl]["sA"]
    sB = params[gmpl]["sB"]
    sC = params[gmpl]["sC"]
    sD = params[gmpl]["sD"]
    sE = params[gmpl]["sE"]
    # sigmatot = params[gmp]["sigmatot"]

    # Define g
    g = 9.80665

    # Convert inputs to arrays
    dists = np.asarray(dists)
    vs30s = np.asarray(vs30s)

    # Initialize the site class "flags"
    ssa = np.zeros(len(vs30s))
    ssb = np.zeros(len(vs30s))
    ssc = np.zeros(len(vs30s))
    ssd = np.zeros(len(vs30s))
    sse = np.zeros(len(vs30s))

    # Class E Vs30 = 0 m/s. We fixed this value to define class E
    idx = (np.abs(vs30s) < 1E-10)
    sse[idx] = 1.0
    # Class D;  Vs30 < 180 m/s.
    idx = (vs30s >= 1E-10) & (vs30s < 180.0)
    ssd[idx] = 1.0
    # SClass C; 180 m/s <= Vs30 <= 360 m/s.
    idx = (vs30s >= 180.0) & (vs30s < 360.0)
    ssc[idx] = 1.0
    # Class B; 360 m/s <= Vs30 <= 800 m/s.
    idx = (vs30s >= 360.0) & (vs30s < 800)
    ssb[idx] = 1.0
    # Class A; Vs30 > 800 m/s.
    idx = (vs30s >= 800.0)
    ssa[idx] = 1.0

    # Compute GMPE
    mag_term = a+b*mag
    path_term = c*np.log10(np.sqrt(dists**2+d**2))
    site_term = sA*ssa + sB*ssb + sC*ssc + sD*ssd + sE*sse
    if gmp in ["pga", "sa0.3", "sa1.0", "sa3.0"]:
        mean = 10.0 ** (mag_term + path_term + site_term)
    else:
        mean = 10.0 ** (mag_term + path_term + site_term)
    
    # Return outputs
    return mean