# Track 2: Ingress, network, Istio, TLS, NIST (second pass, plus merged synthesis)

Run: deep-research workflow wf_bfdab189-595, resumed with a per-angle top-up (top 8 claims each for the three angles the first pass skipped).
The first 25 claims replayed from cache. Totals: 49 claims verified, 47 confirmed, 2 refuted (3 votes each, 2 refutes kill).

## Summary

The brief has the right overall shape. Its Zero Trust intent fits NIST SP 800-207A, which moves controls toward identity-based authentication and authorization enforced by API gateways, sidecar proxies and SPIFFE-style workload identity, layered on top of network controls rather than replacing them. Per-app JWT validation (signature via JWKS, iss/tid, aud, exp/nbf, alg pinning) is also correct and is backed by RFC 8725 and Microsoft's validation guidance. Several core points are wrong or out of date:
- **One token for all apps.** Entra v2 access tokens carry a single aud. Each separately registered API must reject tokens meant for another resource, so the portal needs one token per API, through MSAL silent acquisition, a BFF or on-behalf-of.
- **Groups overage.** Above 200 groups in a JWT, Entra drops the groups claim. Use app roles instead, or handle the overage with Microsoft Graph.
- **NIST timeouts.** The brief's AAL2 values (12 h overall, 30 min inactivity) come from SP 800-63B Rev 3. Rev 4 recommends at most 24 h overall and 1 h inactivity at AAL2; 12 h is the AAL3 limit.
- **Managed NGINX.** Upstream ingress-nginx maintenance ended in March 2026, and Microsoft's patches for the AKS app-routing NGINX end this month (November 2026).
- **SPIFFE/SPIRE with the Istio add-on.** The add-on offers only its built-in Istio CA, with an optional plug-in CA supplied through Key Vault. Microsoft does not document SPIRE integration, and the add-on does not support ambient mode.

The corrected reference architecture:
- **Gateway.** Gateway API ingress on an internal load balancer. Use the Istio add-on's Gateway API if you need mesh mTLS; the managed approuting-istio Gateway cannot run alongside the mesh add-on. Application Gateway for Containers is the other option.
- **Tokens.** A BFF or confidential portal client that gets a separate token for each API.
- **Validation.** Each app validates locally with a standard library that caches JWKS. Pair RequestAuthentication with an AuthorizationPolicy, because RequestAuthentication alone lets requests without a token through.
- **Mesh.** Namespace-wide STRICT PeerAuthentication.
- **Network.** Default-deny NetworkPolicy with explicit allows for DNS, the ingress gateway or load balancer, and Entra endpoints (FQDN rules on Azure CNI powered by Cilium).
- **TLS.** TLS 1.2 minimum with TLS 1.3 enabled, per SP 800-52r2.

## F1 (high, vote 3-0 (merged [0],[3],[6],[10],[22],[24]; [1] 3-0))

The single-token-for-all-apps design is wrong. An Entra access token is issued for one resource and has a single aud; in v2 tokens that aud is the API's client ID. Every web API must reject tokens whose aud is not its own, and accepting another resource's token is the confused-deputy problem. When the client redeems the code, it can request scopes from only one resource (plus OIDC scopes). If a refresh request lists scopes from several resources, Entra returns a token only for the first one. Each separately registered app (app1, app2) therefore needs its own token. Sharing one app registration across apps would make the single token validate, but it gives up per-app least privilege.

**Evidence:** 'The scopes must all be from a single resource, along with OIDC scopes'; 'In v2.0 tokens, this value is always the client ID of the API... reject the token if the value doesn't match'; 'They must only accept tokens containing one of their AppId URIs as the aud claim... confused deputy'; 'An access token can be used only for a specific combination of user, client, and resource'; RFC 8725 §3.9 'the relying party... MUST validate the audience value'.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes
- https://learn.microsoft.com/entra/identity-platform/claims-validation
- https://www.rfc-editor.org/rfc/rfc8725

## F2 (high, vote 3-0 ([1],[2],[12],[13]); [14] 2-1 duplicate of [2])

The correct way to reach several APIs is one token per API. The /authorize request can collect consent for several APIs at once. A refresh token is bound to the user and client, not to a resource, so it can get a separate access token for each consented API, for example with MSAL acquireTokenSilent per scope, through a BFF, or with on-behalf-of. For a public SPA client, refresh tokens issued to a 'spa' redirect URI expire after a fixed 24 hours. Tokens refreshed from them keep that expiry, so the app must redo the auth code flow in a top-level frame every 24 hours; this is usually silent because the existing Entra session is reused. Other client types get a 90-day refresh token by default.

**Evidence:** 'Refresh tokens are bound to a combination of user and client, but aren't tied to a resource'; 'For refresh tokens sent to a redirect URI registered as spa, the refresh token expires after 24 hours... re-run the authorization code flow'; '24 hours for single-page applications... 90 days for all other scenarios'. The verified claims did not include the IETF Browser-Based Apps BCP. The BFF recommendation is inference from these constraints.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens

## F3 (high, vote 3-0 ([4],[15],[16],[17]))

Groups claims overflow. If a user is in more than 200 groups (JWT), 150 (SAML) or 6 (implicit flow), Entra leaves out the groups claim and emits an overage indicator instead: _claim_names/_claim_sources, or hasgroups in the implicit flow. The app must then call Microsoft Graph (transitiveMemberOf), which needs egress to Graph and OBO or app permissions. It should not rely on _claim_sources, which can point to the legacy AAD Graph. Overage can be avoided in two ways. One is 'Groups assigned to the application', which covers direct membership only and needs Entra P1. The other is app roles, which put a roles claim in the access token; this is the recommended authorization basis for the brief's apps.

**Evidence:** '(150 for SAML tokens, 200 for JWT tokens)... doesn't emit the groups claim'; 'check for the existence of a hasgroups claim or a _claim_names claim... your app must use Microsoft Graph'; 'Groups assigned to the application option doesn't support indirect membership. Group assignment requires at least a P1'.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles

## F4 (high, vote 3-0 ([5],[7]))

Identity claims and token version. Use oid (immutable, the same across apps in a tenant) or sub (pairwise per app) as the authorization or database key. upn and preferred_username are for display and login hints only, and upn appears in v2 tokens only as an optional claim. The resource's app manifest (api.requestedAccessTokenVersion, formerly accessTokenAcceptedVersion) sets the token version: null or 1 gives v1, 2 gives v2, whichever endpoint the client calls. A validator must use the issuer metadata that matches the token's ver. Recommendation: set version 2 on every API so that aud is the client ID and iss is the v2.0 issuer.

**Evidence:** 'upn ... Only use for display purposes'; 'The values of null and 1 result in v1.0 tokens, and the value of 2 results in v2.0 tokens... a client calling the v1.0 endpoint... receives a v2.0 access token'.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens

## F5 (high, vote 3-0 ([9],[11]))

Access-token lifetime and revocation gap. By default an access token lives for a random 60-90 minutes (75 on average); the exact value varies with client, resource and Conditional Access. When both the client and the resource support CAE, the lifetime can be extended automatically to 24-28 hours, with near-real-time revocation on critical events. A custom API gets this revocation only if it implements the CAE claims-challenge flow; otherwise a stolen bearer token stays valid until it expires.

**Evidence:** 'random value ranging between 60-90 minutes (75 minutes on average)'; 'When both the client and the resource support CAE... may be automatically extended to 24-28 hours... revoked in near real time'.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes

## F6 (high, vote 3-0 ([8],[18],[19],[20],[21],[23]))

Per-app JWT validation and JWKS caching. Pin the accepted algorithms (for example RS256 only): RFC 8725 requires libraries to let callers set the allowed algorithms, with exactly one algorithm per key. Validate iss and tid against the expected tenant, because Entra's common JWKS keys are shared across tenants. Validate sub. Pick the signing key by kid; v2 tokens carry only kid, not x5t. Entra rotates signing keys on no fixed schedule and may rotate immediately in an emergency, so never pin keys. Use standard libraries (IdentityModel BaseConfigurationManager, which Microsoft.Identity.Web and JwtBearer use). They keep the last known good configuration if a fetch fails and refresh about every 12 h ± 1 h. Microsoft's guidance for custom caches: cache each key by kid with a 24 h TTL, refresh every hour in the background, and refresh on an unknown kid at most once every 5 minutes. Validators therefore need egress to login.microsoftonline.com, but a short outage does not break validation.

**Evidence:** 'There's no set or guaranteed time between these key rolls'; 'time-to-live of keys in the cache should be configured to 24 hours, with refreshes happening every hour'; 'continues to operate with the last known good configuration'; 'Libraries MUST enable the caller to specify a supported set of algorithms'. The verified claims did not cover PyJWT PyJWKClient or jose behaviour.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/entra/identity-platform/signing-key-rollover
- https://www.rfc-editor.org/rfc/rfc8725

## F7 (high, vote 3-0 ([25],[26],[27],[28],[29]))

Ingress on AKS. Upstream ingress-nginx maintenance ended in March 2026. Microsoft supports the application routing add-on's NGINX only through November 2026, with critical security patches only, so a design based on managed NGINX reaches end of support this month. The supported successor is the application routing Gateway API implementation, GatewayClass approuting-istio: a lightweight Istio control plane with no Istio CRDs and no sidecar injection. It cannot run alongside the Istio service mesh add-on, whose *.istio.io CRDs must be removed first, so it cannot provide STRICT mTLS. If you need a mesh, use Gateway API ingress through the Istio add-on (GatewayClass istio) or Application Gateway for Containers.

**Evidence:** 'maintenance that ended in March 2026... critical security patches... through November 2026'; 'only reconciles Gateway API resources belonging to the approuting-istio GatewayClass, with no support for Istio CRDs or data-plane sidecar injection'; 'The application routing Gateway API control plane fails to start while those CRDs are present'. The verified claims did not cover --watch-namespace, default-backend or wildcard host risk, or the internal LB annotation.

**Sources:**
- https://blog.aks.azure.com/2025/11/13/ingress-nginx-update
- https://learn.microsoft.com/azure/aks/app-routing-nginx-to-gateway-api-migration
- https://learn.microsoft.com/azure/aks/app-routing-gateway-api

## F8 (high, vote 3-0 ([30],[31]))

NetworkPolicy and egress. On Cilium (Azure CNI powered by Cilium), a namespace default-deny-ingress policy also blocks traffic arriving through LoadBalancer or NodePort Services with externalTrafficPolicy=Cluster. Azure NPM did not enforce policy on that path. You must explicitly allow traffic from the ingress gateway or controller pods and the internal LB source ranges. FQDN egress filtering for Entra and JWKS hosts works through the ACNS Security Agent DNS proxy, and only for pods that have FQDN policies. Those policies must allow kube-dns on port 53 and include a dns matchPattern rule, or the FQDN-to-IP mappings are never learned. Standard Kubernetes NetworkPolicy cannot match FQDNs.

**Evidence:** 'With Cilium: All ingress traffic is blocked, including traffic via NodePort or LoadBalancer, unless explicitly allowed'; 'The Cilium Agent marks DNS request packets... redirecting them to the ACNS Security Agent... only for pods that are enforcing FQDN policies'. One claim was refuted 1-2: that FQDN filtering requires paid ACNS and Kubernetes 1.29+. The exact licensing and version prerequisites remain unverified.

**Sources:**
- https://learn.microsoft.com/en-us/azure/aks/migrate-from-npm-to-cilium-network-policy
- https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts

## F9 (high, vote 3-0 ([32] medium-evidence,[33],[34],[35],[36],[37]))

Limits of the AKS Istio add-on. It does not support ambient (sidecar-less) mode, so on the add-on you use sidecars. It blocks the ProxyConfig, WorkloadEntry, WorkloadGroup, IstioOperator and WasmPlugin resources and supports only part of MeshConfig. By default its Istio CA signs workload certificates with a self-signed root. To bring your own CA, generate the root cert, intermediate cert and key, and chain offline, store them as Key Vault secrets synced by the Secrets Store CSI add-on, and pass them to 'az aks mesh enable'. An existing self-signed mesh cannot be switched to a plug-in CA in place; the mesh must be disabled and re-enabled. Workload certificates last 24 hours by default. Microsoft documents no SPIFFE/SPIRE integration. That SPIRE is therefore impractical on the add-on is inference: it would need customization the add-on blocks.

**Evidence:** 'The add-on doesn't yet support the sidecar-less Ambient mode'; 'Customization of mesh through... ProxyConfig, WorkloadEntry, WorkloadGroup, IstioOperator, WasmPlugin is currently blocked'; 'by default the Istio CA generates a self-signed root'; 'switching to plugin CA is not supported'; 'valid for 24 hours by default'.

**Sources:**
- https://learn.microsoft.com/en-us/azure/aks/istio-about
- https://learn.microsoft.com/en-us/azure/aks/istio-plugin-ca

## F10 (medium, vote 2-1 ([38]))

Istio RequestAuthentication on its own does not enforce authentication. It rejects requests with an invalid token, but requests with no token are accepted without an identity. Pair it with an AuthorizationPolicy that requires requestPrincipals (for example ["https://login.microsoftonline.com/<tid>/v2.0/*"]) and checks claims such as aud and roles.

**Evidence:** 'A request that does not contain any authentication credentials will be accepted but will not have any authenticated identity. To restrict access to authenticated requests only, this should be accompanied by an authorization rule.' The vote was split, but the primary text is unambiguous.

**Sources:**
- https://istio.io/latest/docs/reference/config/security/request_authentication/

## F11 (high, vote 3-0 ([39],[40],[41]))

NIST SP 800-207A (Sept 2023) supports identity-based segmentation. It moves the focus from network-parameter segmentation to authentication and authorization based on application and service identities, added to network controls rather than replacing them. It names API gateways, sidecar proxies and SPIFFE-style identity infrastructure as the enforcement platform. Mapping this to the brief: the Istio ingress gateway plus sidecars (or app middleware) act as PEPs, with Entra and the policies as the PDP. Keep NetworkPolicy as an extra layer. The mapping is inference; NIST does not endorse products.

**Evidence:** 'change in focus from security controls based on segmentation and isolation using network parameters... to identities... in addition to the underlying network parameters'; 'API gateways, sidecar proxies, and application identity infrastructures (e.g., SPIFFE)'. The verified claims did not include the SP 800-207 base tenets.

**Sources:**
- https://csrc.nist.gov/pubs/sp/800/207/a/final

## F12 (high, vote 3-0 ([44],[45],[46]))

Correction to the brief's NIST SP 800-63B Rev 4 figures (final, Aug 2025). At AAL2 the overall reauthentication timeout SHALL be set and SHOULD be at most 24 h, with an inactivity timeout of at most 1 h. At AAL3 the overall timeout SHALL be at most 12 h, with inactivity of at most 15 min. The brief's 12 h / 30 min for AAL2 is the Rev 3 rule; it is stricter than Rev 4 and still complies, but it misstates Rev 4. AAL2 verifiers SHALL offer at least one phishing-resistant option, such as passkeys, FIDO2 or certificate-based auth through Entra authentication strengths, though users are not required to use it.

**Evidence:** 'SHOULD be no more than 24 hours at AAL2... inactivity timeout SHOULD be no more than 1 hour'; 'At AAL3... SHALL be no more than 12 hours... 15 minutes'; 'Verifiers SHALL offer at least one phishing-resistant authentication option at AAL2'. The Entra Conditional Access mapping is inference, not verified.

**Sources:**
- https://pages.nist.gov/800-63-4/sp800-63b.html

## F13 (medium, vote 3-0 ([42],[43]))

TLS baseline. SP 800-52 Rev 2 requires all government TLS servers and clients to support TLS 1.2 with FIPS-based cipher suites, and requires TLS 1.3 support by 1 January 2024; the binding TLS 1.3 text is for servers, while clients are only recommended to support it. Configure the gateway and mesh with TLS 1.2 as the minimum, TLS 1.3 enabled, and ECDHE+AES-GCM suites. 'Minimum' is a practical reading: the abstract says 'support', and the body is recalled from memory and was not re-checked in this run.

**Evidence:** 'requires that TLS 1.2 configured with FIPS-based cipher suites be supported by all government TLS servers and clients, and requires support for TLS 1.3 by January 1, 2024.' The full PDF was not fetched. The page notes the document has been under review since May 2026.

**Sources:**
- https://csrc.nist.gov/pubs/sp/800/52/r2/final

## Refuted

- (1-2) AKS FQDN-based egress filtering (needed to allow login.microsoftonline.com / JWKS endpoints by name rather than IP) requires Azure CNI Powered by Cilium, Kubernetes 1.29+, and Advanced Container Networking Services, which is a paid add-on. It is not part of standard Kubernetes NetworkPolicy. - https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts
- (0-3) The Istio add-on for AKS sorts features and MeshConfig options into allowed, supported and blocked. Blocked options are rejected at the API server by admission webhooks that the add-on manages, and allowed options work but Azure support does not cover them. So whether SPIFFE/SPIRE or a custom CA is possible depends on this classification, not on upstream Istio. - https://learn.microsoft.com/en-us/azure/aks/istio-support-policy

## Caveats

Time sensitivity: today is 2026-11-09. Microsoft's support for the app-routing NGINX ends this month, upstream ingress-nginx is already retired, and the AKS Gateway API, ambient and preview offerings are changing fast. Gaps: no verified claims covered ingress-nginx --watch-namespace or IngressClass scoping, default-backend or wildcard risks, TLS secret scoping, the internal LB annotation, cert-manager or trust-manager, the Key Vault CSI driver for app TLS, Envoy JWT filter JWKS caching, PyJWT/jose library behaviour, the IETF Browser-Based Apps BCP, RFC 9068 and 6750 (cited only secondhand in verifier notes), SP 800-207 base tenets, or the Azure NPM deprecation timeline. Recommendations in those areas are inference or need separate verification. Two claims were refuted: (1) that FQDN filtering needs paid ACNS plus Kubernetes 1.29+, so its prerequisites remain uncertain; (2) a characterisation of the Istio add-on support-policy tiers. The SP 800-52r2 'minimum' and client TLS 1.3 nuances rest on the verifier's memory of the PDF. Claim [38] passed 2-1. The statement that SPIRE cannot be used on the add-on is inference from the blocked customizations, not a Microsoft statement. Reports of managed ambient previews (Azure Kubernetes Application Network) were not confirmed from primary sources.

## Open questions

- What exact licensing, cluster version and data-plane prerequisites does AKS FQDN filtering (ACNS on Cilium) have, and is there a supported alternative such as Azure Firewall FQDN rules or service tags for allowing egress to login.microsoftonline.com and graph.microsoft.com?
- How do Envoy's jwt_authn remote JWKS cache duration and refetch-on-unknown-kid behaviour in the AKS Istio add-on compare with Microsoft's 24 h TTL, 1 h refresh and 5 min unknown-kid guidance, and what happens during a login.microsoftonline.com outage?
- Can a custom internal API implement CAE claims challenges in practice (Microsoft.Identity.Web support, client requirements), and how short do access tokens need to be without CAE to meet a given revocation SLA?
- If SPIFFE/SPIRE federation is a hard requirement, is self-managed open-source Istio (sidecar or ambient) or the previewed managed ambient offering a production-ready path on AKS?

## Verification log

- "At code redemption, the scope parameter…": 3-0 ✓
- "The /authorize request can collect conse…": 3-0 ✓
- "For refresh tokens sent to a 'spa' redir…": 3-0 ✓
- "An Entra access token has a single audie…": 3-0 ✓
- "Groups overage: if a user belongs to mor…": 3-0 ✓
- "upn and preferred_username are mutable a…": 3-0 ✓
- "An Entra access token is meant for a sin…": 3-0 ✓
- "The resource (API) app registration sets…": 3-0 ✓
- "Entra rotates its signing keys periodica…": 3-0 ✓
- "Entra access tokens by default get a ran…": 3-0 ✓
- "An Entra access token is bound to one co…": 3-0 ✓
- "When both the client and the resource su…": 3-0 ✓
- "Entra refresh tokens are bound to the us…": 3-0 ✓
- "The default refresh token lifetime is 24…": 3-0 ✓
- "Refresh tokens sent to a redirect URI re…": 2-1 ✓
- "Entra ID caps the groups claim at 200 gr…": 3-0 ✓
- "Overage is signalled by a hasgroups clai…": 3-0 ✓
- "Two ways to avoid overage: emit only 'Gr…": 3-0 ✓
- "Entra signing keys roll over periodicall…": 3-0 ✓
- "For custom JWKS caching, Microsoft recom…": 3-0 ✓
- "Microsoft recommends standard libraries…": 3-0 ✓
- "JWT libraries must let callers specify (…": 3-0 ✓
- "A relying party must validate the aud cl…": 3-0 ✓
- "Applications must check that the signing…": 3-0 ✓
- "Each web API must verify that the token'…": 3-0 ✓
- "Upstream Kubernetes ingress-nginx is bei…": 3-0 ✓
- "Microsoft will officially support Ingres…": 3-0 ✓
- "Upstream maintenance of the Ingress NGIN…": 3-0 ✓
- "On AKS, the supported successor is the a…": 3-0 ✓
- "The application routing Gateway API impl…": 3-0 ✓
- "AKS FQDN-based egress filtering (needed…": 1-2 ✗
- "FQDN filtering works by redirecting the…": 3-0 ✓
- "On Cilium, ingress NetworkPolicy also ap…": 3-0 ✓
- "The AKS Istio add-on does not support Is…": 3-0 ✓
- "Mesh customization through ProxyConfig,…": 3-0 ✓
- "By default the AKS Istio add-on's Istio…": 3-0 ✓
- "Plug-in CA inputs (root-cert, ca-cert, c…": 3-0 ✓
- "You cannot switch an existing Istio add-…": 3-0 ✓
- "Workload leaf certificates issued by the…": 3-0 ✓
- "The Istio add-on for AKS sorts features…": 0-3 ✗
- "An Istio RequestAuthentication on its ow…": 2-1 ✓
- "NIST SP 800-207A (Chandramouli/NIST and…": 3-0 ✓
- "SP 800-207A moves the focus away from se…": 3-0 ✓
- "SP 800-207A says the enforcement platfor…": 3-0 ✓
- "NIST SP 800-52 Rev. 2 requires all gover…": 3-0 ✓
- "NIST SP 800-52 Rev. 2 requires governmen…": 3-0 ✓
- "At AAL2 in SP 800-63B-4, the overall rea…": 3-0 ✓
- "The 12-hour limit belongs to AAL3, where…": 3-0 ✓
- "At AAL2, verifiers must offer at least o…": 3-0 ✓
