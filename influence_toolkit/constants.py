# badger wallets
TREASURY_VAULT_MSIG = "0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e"
VOTER_MSIG = "0xA9ed98B5Fb8428d68664f3C5027c62A10d45826b"
BADGER_DELEGATE = "0x14f83ff95d4ec5e8812ddf42da1232b0ba1015e6"

# aura
AURA = "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF"
VLAURA = "0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC"

PROXY_AURA_VOTER = "0xaF52695E1bB01A16D33D7194C28C42b10e0Dbec2"

# balancer
VEBAL = "0xC128a9954e6c874eA3d62ce62B468bA073093F25"
BALANCER_VAULT = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
BALANCER_GAUGE_CONTROLLER = "0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD"

BADGER_WBTC_POOL = "0xb460DAa847c45f1C4a41cb05BFB3b51c92e41B36"
BADGER_RETH_POOL = "0x1ee442b5326009Bb18F2F472d3e0061513d1A0fF"
DIGG_WBTC_GRAVI_POOL = "0x8eB6c82C3081bBBd45DcAC5afA631aaC53478b7C"

REWARDS_BADGER_WBTC = "0x4efc8ded860bc472fa8d938dc3fd4946bc1a0a18"
REWARDS_BADGER_RETH = "0xaad4ee162dbc9c25cca26ba4340b36e3ef7c1a80"
REWARDS_DIGG_WBTC_GRAVI = "0xd7c9c6922db15f47ef3131f2830d8e87f7637210"

POOL_ID_BADGER = "0xb460daa847c45f1c4a41cb05bfb3b51c92e41b36000200000000000000000194"
POOL_ID_DIGG = "0x8eb6c82c3081bbbd45dcac5afa631aac53478b7c000100000000000000000270"
POOL_ID_BADGE_RETH = "0x76fcf0e8c7ff37a47a799fa2cd4c13cde0d981c90002000000000000000003d2"

BALANCER_BADGER_WBTC_GAUGE = "0x3F29e69955E5202759208DD0C5E0BA55ff934814"
BALANCER_DIGG_GRAVI_GAUGE = "0xE5f24cD43f77fadF4dB33Dab44EB25774159AC66"
BALANCER_BADGER_RETH_GAUGE = "0x87012b0C3257423fD74a5986F81a0f1954C17a1d"

# curve/convex
CURVE_BADGER_FRAXBP_LP = "0x09b2E090531228d1b8E3d948C73b990Cb6e60720"
CURVE_BADGER_FRAXBP_POOL = "0x13B876C26Ad6d21cb87AE459EaF6d7A1b788A113"

PRIVATE_VAULT_BADGER_FRAXBP_TREASURY = "0xa895B89D74a6BC23a284a0526e123ea776674cF5"

# frax
FRAX_GAUGE_CONTROLLER = "0x3669C421b77340B2979d1A00a792CC2ee0FcE737"
BADGER_FRAXBP_GAUGE = "0x5a92EF27f4baA7C766aee6d751f754EBdEBd9fae"

# uniswap
BADGER_WBTC_UNIV3 = "0xe15e6583425700993bd08F51bF6e7B73cd5da91B"

# bunni
WBTC_BADGER_GAUGE = "0xFf780599310ccd337Da4D4804fE31A75c2a66a81"

# budgets
MAX_COUNCIL_BRIBE = 16_000

# emissions and fees
BALANCER_EMISSIONS = 121_930
FXS_DAILY_EMISSIONS = 6250
AURA_FEE = 0.25
CVX_FEE = 0.17
COUNCIL_FEE = 0.1

# gauge caps
GAUGE_CAP_TWO_PCT = 0.02
GAUGE_CAP_TEN_PCT = 0.1

# dataframe helpers
DF_HEADER = ["tvl", "capture"]
POOL_INDEXES = ["WBTC/BADGER", "DIGG/GRAVI/WBTC", "BADGER/RETH", "BADGER/FRAXBP", "BUNNI Gauge"]

# endpoints
BALANCER_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
BUNNI_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/bunniapp/bunni-mainnet"
SNAPSHOT_SUBGRAPH = "https://hub.snapshot.org/graphql?"
LLAMA_DASHBOARD_URL = "https://api.llama.airforce//dashboard"
CURVE_FACTORY_URL = "https://api.curve.fi/api/getPools/ethereum/factory-crypto"
