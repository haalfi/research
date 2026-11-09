# Track 1: Entra ID identity, tokens, JWT validation (first pass)

Run: deep-research workflow wf_bfdab189-595, first pass. 26 sources fetched, 129 claims extracted, top 25 verified (3 votes each).
All verified claims fell in brief items 1-3 and part of 9; items 4-8 were cut by the global top-25 cap and are re-verified in a second pass (see 02).

## Summary

The verified evidence covers only parts of the brief: identity and tokens (items 1-3) and the token-lifetime and revocation part of item 9. On those parts, the brief's central design is wrong. Entra ID issues each access token for a single resource. At code redemption the scope must come from one resource, aud is a single value, and Microsoft, RFC 8725 and RFC 9068 all require each API to reject a token whose aud is not its own. So one bearer token forwarded to app1 and app2 fails validation at whichever app it was not issued for, or, if aud checks are relaxed, creates a confused-deputy weakness. The fix is a separate token per API. The portal can get these from one consented refresh token, because Entra refresh tokens are bound to user plus client, not to a resource. Better still, a BFF or on-behalf-of exchange keeps tokens out of the browser and avoids the 24-hour hard limit on SPA refresh tokens. Two more gaps need attention. Group-based authorization needs a plan for groups overage (more than 200 groups in a JWT), using app roles or assigned-groups filtering, or else the API needs Graph egress. Each validator needs egress to login.microsoftonline.com for JWKS rollover and must pin algorithms and check iss, tid, aud, exp and nbf. No claim about ingress, NetworkPolicy, Istio, SPIFFE, TLS (NIST SP 800-52) or the NIST ZTA and AAL mappings (items 4-8) survived verification, so this synthesis cannot confirm or refute them.

## F1 (high, vote 3-0 (merged claims 0, 3, 6, 10, 22, 24))

One access token cannot serve several separately registered downstream APIs. Entra issues each token for one resource, its aud is a single value (in v2.0 tokens, the API's client ID GUID; in v1.0 tokens, an App ID URI), and each API must reject a token whose aud does not match it. Accepting another resource's token is the confused-deputy problem. The brief's 'one token propagated to app1/app2' design is therefore wrong. Each API needs its own token.

**Evidence:** Auth code flow doc: at redemption, 'The scopes must all be from a single resource, along with OIDC scopes'. Access token claims reference: aud is a String, and 'In v2.0 tokens, this value is always the client ID of the API... reject the token if the value doesn't match the intended audience'. Access tokens doc: APIs 'must only accept tokens containing one of their AppId URIs as the aud claim... Validating and accepting tokens meant for another resource is an example of the confused deputy problem'. Configurable token lifetimes: 'An access token can be used only for a specific combination of user, client, and resource'. RFC 8725 section 3.9: the relying party 'MUST validate the audience value' and MUST reject a JWT whose audience is missing or does not match. RFC 9068 section 4 says the same; the verifier cited it from its own knowledge and did not fetch it. Caveat: app1 and app2 could share one app registration, and so one aud, but that merges them into one resource and weakens least privilege.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes
- https://learn.microsoft.com/entra/identity-platform/claims-validation
- https://www.rfc-editor.org/rfc/rfc8725

## F2 (high, vote 3-0 (merged claims 1, 12))

The corrected pattern is one token per API, obtained from a single sign-in. /authorize can collect consent for several APIs at once. Refresh tokens are bound to user plus client, not to a resource, so the client can redeem them for a separate access token per API (for example, MSAL acquireTokenSilent per scope set, or a BFF). If a refresh request mixes scopes from several resources, Entra issues a token only for the resource of the first scope.

**Evidence:** Auth code flow doc: for /authorize, scope 'can cover multiple resources'. 'If the scopes specified in this request span multiple resource server, then the Microsoft identity platform returns a token for the resource specified in the first scope.' Refresh tokens doc: 'Refresh tokens are bound to a combination of user and client, but aren't tied to a resource or tenant. A client can use a refresh token to acquire access tokens across any combination of resource and tenant where it has permission.'

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens

## F3 (high, vote 3-0 on claims 2 and 13; 2-1 on claim 14, which only adds the top-level-frame detail from the same page)

Default token lifetimes. A refresh token issued to a redirect URI registered as 'spa' has a hard 24-hour lifetime that carries over to later refresh tokens, so the SPA must rerun the auth code flow in a top-level frame every 24 hours; this usually happens silently through the Entra session cookie. Other refresh tokens last 90 days by default, except for the email one-time-passcode flow, which is 24 hours. This favours a BFF (confidential web client) over a pure SPA for the portal.

**Evidence:** 'For refresh tokens sent to a redirect URI registered as spa, the refresh token expires after 24 hours. Additional refresh tokens acquired using the initial refresh token carries over that expiration time... re-run the authorization code flow... every 24 hours.' Token lifetime section: '24 hours for single-page applications... 90 days for all other scenarios.' The same note: 'The browser must visit the sign-in page in a top-level frame.' The BFF recommendation is inference. The IETF OAuth 2.0 for Browser-Based Apps BCP was not among the verified sources.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
- https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens

## F4 (high, vote 3-0 (claims 9, 11))

By default, access tokens get a random lifetime of 60-90 minutes (75 on average), which varies with the client, the resource and Conditional Access. When both client and resource support Continuous Access Evaluation (CAE), Entra may automatically extend the lifetime to 24-28 hours and revokes these tokens in near real time on critical events. A custom API such as app1 or app2 gets that revocation only if it implements the CAE claims-challenge flow.

**Evidence:** 'an access token's default lifetime is assigned a random value ranging between 60-90 minutes (75 minutes on average)...' 'When both the client and the resource support CAE..., the token lifetime may be automatically extended to 24-28 hours... revoked in near real time in response to critical events such as account disablement and password changes.' The verifier noted that Configurable Token Lifetime policy still caps access tokens below 24 hours. That an API needs its own claims-challenge implementation to support CAE is a verifier caveat (inference).

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes

## F5 (high, vote 3-0 (claim 5))

Which identity claims to use. Use oid (immutable, the same across apps in a tenant) or sub (immutable, pairwise per application) as authorization and database keys. upn and preferred_username are for display and username hints only. upn is a v1.0 basic claim and appears in v2.0 tokens only when configured as an optional claim.

**Evidence:** upn: 'Only use for display purposes and providing username hints in reauthentication scenarios.' preferred_username: 'Since this value is mutable, don't use it to make authorization decisions.' oid: 'Two different applications signing in the same user receive the same value in the oid claim.' sub: 'a pairwise identifier that's unique to a particular application ID.' v1.0 basic claims (including upn) are absent from v2.0 tokens by default and must be requested as optional claims.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference

## F6 (high, vote 3-0 (merged claims 4, 15, 16))

Groups overage. Above 200 groups (JWT), 150 (SAML) or 6 (implicit flow), Entra omits the groups claim. It signals overage with hasgroups (implicit flow) or _claim_names/_claim_sources. The app must then call Microsoft Graph (user transitiveMemberOf) rather than trust the _claim_sources URL, which may point to legacy Azure AD Graph. An API that authorizes on groups therefore needs Graph egress and OBO or app permissions, unless overage is designed out.

**Evidence:** 'If a user is a member of more groups than the overage limit (150 for SAML tokens, 200 for JWT tokens), then Microsoft Entra ID doesn't emit the groups claim...' and 'Six groups when using the implicit flow'. 'check for the existence of a hasgroups claim or a _claim_names claim with a groups member... your app must use Microsoft Graph.' Note: 'The URL returned will be an Azure AD Graph URL... use the idtyp optional claim... to construct a Microsoft Graph URL.' The Microsoft page contradicts itself on whether the URL points to Microsoft Graph or Azure AD Graph. The need for Graph egress is inference.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles

## F7 (high, vote 3-0 (claim 17))

Two ways to avoid overage. (a) Set the groups claim to 'Groups assigned to the application': direct membership only, no nested groups, and at least Entra P1 required. (b) Define app roles with Users/Groups as allowed member types, so a roles claim appears in the API's access token. App roles are the preferred authorization signal for app1 and app2.

**Evidence:** 'the Groups assigned to the application option doesn't support indirect membership. Group assignment requires at least a P1 level license.' 'Another way to avoid the group overage problem is for the app to define app roles that allow users and groups as member types... Your app gets a roles claim in your token (ID token for app, access token for APIs).' The P1 requirement also applies to assigning groups to app roles. Preferring app roles is a synthesis recommendation.

**Sources:**
- https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles

## F8 (high, vote 3-0 (claim 7))

The resource (API) registration sets the token version: requestedAccessTokenVersion (called accessTokenAcceptedVersion in the legacy manifest) of null or 1 gives v1.0 tokens, and 2 gives v2.0 tokens, whichever endpoint the client calls. Validators must use the OIDC metadata and issuer for the token's actual version. Recommendation: set it to 2 on every API registration so that aud is the client ID and iss is the v2.0 issuer.

**Evidence:** 'The values of null and 1 result in v1.0 tokens, and the value of 2 results in v2.0 tokens... when the value of requestedAccessTokenVersion is 2, a client calling the v1.0 endpoint to get a token for that resource receives a v2.0 access token.' A validator checking a v1.0 token must read the v1.0 metadata 'even if the authority configured for your web API is a v2.0 authority'. Setting it to 2 everywhere is a recommendation (inference).

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens

## F9 (high, vote 3-0 (merged claims 21, 22, 23))

Per-app JWT validation rules (RFC 8725). Pin the accepted algorithms (for example RS256 only). Each key is used with exactly one algorithm. Verify that the signing key belongs to the expected issuer, which on Entra means checking iss and tid against the expected tenant, because common JWKS keys are shared across tenants. Validate sub and aud, and reject on any mismatch.

**Evidence:** Section 3.1: 'Libraries MUST enable the caller to specify a supported set of algorithms... each key MUST be used with exactly one algorithm'. Section 3.8: 'the application MUST validate that the cryptographic keys used... belong to the issuer. If they do not, the application MUST reject the JWT.' Section 3.9: audience MUST be validated. The MUSTs bind libraries, so the app still has to pass an explicit algorithm list (for example PyJWT algorithms=['RS256']). Applying 3.8 to tid is inference.

**Sources:**
- https://www.rfc-editor.org/rfc/rfc8725

## F10 (high, vote 3-0 (merged claims 8, 18, 19, 20))

JWKS caching and signing-key rollover. Entra rotates signing keys with no guaranteed interval and may roll them immediately in an emergency, so validators must select the key by kid (v2.0 tokens carry only kid, no x5t) and must not hardcode keys. Prefer standard libraries (IdentityModel BaseConfigurationManager, which Microsoft.Identity.Web and JwtBearer use). These keep the last known good configuration when a fetch fails and refresh about every 12 hours plus or minus 1 hour. A custom implementation should cache keys by kid with a 24-hour TTL, refresh hourly in the background, and refresh on an unknown kid or tid at most once every 5 minutes. Each validator (or the Envoy/Istio proxy) therefore needs egress to login.microsoftonline.com, but a short outage does not break validation right away.

**Evidence:** 'Microsoft Entra ID rotates the possible set of keys on a periodic basis... A reasonable frequency to check for updates... is every 24 hours.' 'v2.0 tokens contain only the kid claim.' 'in the case of an emergency, could be rolled over immediately. There's no set or guaranteed time between these key rolls.' 'The time-to-live of keys in the cache should be configured to 24 hours, with refreshes happening every hour.' 'The system continues to operate with the last known good configuration if new data can't be fetched.' On refresh interval: '(recommend 12 h with a jitter of plus or minus 1 h)'. The 'must' slightly overstates Microsoft's 'should'. That Microsoft.Identity.Web uses BaseConfigurationManager is the verifier's inference. That the validators need egress, including the Envoy/Istio proxy, is inference.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/entra/identity-platform/signing-key-rollover

## Caveats

Coverage is uneven. All 25 confirmed claims concern Entra tokens and JWT validation (brief items 1-3, plus the CAE and JWKS-caching parts of item 9). No claim about items 4-8 survived verification: ingress-nginx scoping and its retirement status, the AKS app-routing add-on, Gateway API, internal LB annotations, NetworkPolicy default-deny and DNS/FQDN egress, Cilium/ACNS, the Azure NPM deprecation, Istio STRICT mTLS, SPIFFE/SPIRE with the Istio add-on, RequestAuthentication behaviour with no token, NIST SP 800-52r2, cert-manager/trust-manager/Key Vault CSI, and the NIST SP 800-207/207A/63B-4 mappings. The report must not present conclusions on these as verified. They are unverified or need further runs. The IETF Browser-Based Apps BCP and RFC 9068 were not fetched by the verifiers (RFC 9068 was cited from the verifier's own knowledge), so the BFF recommendation rests on Entra's SPA refresh limits plus inference. The sources are almost all Microsoft Learn pages, which are primary and current (updated 2025-2026) but are a single vendor. Microsoft's own pages are inconsistent about whether the overage URL points to Azure AD Graph or Microsoft Graph. Lifetime figures (60-90 min, 24h SPA refresh, CAE 24-28h) and Microsoft's 'as of publication' notes (no nested groups for assigned groups) can change. Several conclusions are labelled inference: Graph egress requirements, the tid check, and the Microsoft.Identity.Web internals. The 'one token cannot serve many apps' conclusion holds for separately registered APIs. A shared app registration would technically work but merges the apps into one resource.

## Open questions

- Does the Istio-based service mesh add-on for AKS support a SPIFFE/SPIRE or external plugin CA, and how does a RequestAuthentication + AuthorizationPolicy setup handle requests with no token and the Envoy JWKS cache relative to Entra's emergency key rollover?
- With default-deny egress, how should JWKS and Graph egress to login.microsoftonline.com and graph.microsoft.com be allowed? Options include Cilium FQDN policies or Advanced Container Networking Services on Azure CNI powered by Cilium, versus an egress gateway or firewall, given that plain Kubernetes NetworkPolicy cannot express FQDNs.
- What is the current status of the ingress-nginx retirement (announced for March 2026) and of the AKS application routing add-on, and should the portal entry point move to Gateway API (Istio gateway or Application Gateway for Containers) on an internal load balancer?
- How do the brief's reauthentication and token-handling design map to the final NIST SP 800-63B Rev 4 AAL2 requirements (reauthentication intervals, phishing-resistant options) and to Entra Conditional Access authentication strengths and sign-in frequency?

## Sources fetched

- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/EN-US/azure/active-directory/develop/refresh-tokens (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles (Entra ID tokens and audience constraints (primary docs))
- [primary] https://learn.microsoft.com/entra/identity-platform/signing-key-rollover (JWT validation standards and key rollover)
- [primary] https://www.rfc-editor.org/rfc/rfc8725 (JWT validation standards and key rollover)
- [primary] https://learn.microsoft.com/entra/identity-platform/claims-validation (JWT validation standards and key rollover)
- [primary] https://learn.microsoft.com/entra/identity-platform/access-token-claims-reference (JWT validation standards and key rollover)
- [primary] https://rfc-editor.org/rfc/rfc9068.html (JWT validation standards and key rollover)
- [primary] https://osv.dev/GHSA-fhv5-28vv-h8m8 (JWT validation standards and key rollover)
- [primary] https://blog.aks.azure.com/2025/11/13/ingress-nginx-update (AKS ingress, network policy and egress (practitioner and recent news))
- [primary] https://learn.microsoft.com/azure/aks/app-routing-nginx-to-gateway-api-migration (AKS ingress, network policy and egress (practitioner and recent news))
- [primary] https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts (AKS ingress, network policy and egress (practitioner and recent news))
- [primary] https://learn.microsoft.com/en-us/azure/aks/migrate-from-npm-to-cilium-network-policy (AKS ingress, network policy and egress (practitioner and recent news))
- [primary] https://learn.microsoft.com/en-us/azure/aks/istio-about (Istio add-on for AKS: mTLS, JWT and SPIFFE limits)
- [primary] https://learn.microsoft.com/en-us/azure/aks/istio-plugin-ca (Istio add-on for AKS: mTLS, JWT and SPIFFE limits)
- [primary] https://learn.microsoft.com/en-us/azure/aks/istio-support-policy (Istio add-on for AKS: mTLS, JWT and SPIFFE limits)
- [primary] https://istio.io/latest/docs/reference/config/security/request_authentication/ (Istio add-on for AKS: mTLS, JWT and SPIFFE limits)
- [primary] https://istio.io/latest/docs/tasks/security/authentication/authn-policy/ (Istio add-on for AKS: mTLS, JWT and SPIFFE limits)
- [primary] https://csrc.nist.gov/pubs/sp/800/207/a/final (NIST zero trust, TLS and authenticator assurance compliance)
- [primary] https://csrc.nist.gov/pubs/sp/800/52/r2/final (NIST zero trust, TLS and authenticator assurance compliance)
- [primary] https://pages.nist.gov/800-63-4/sp800-63b.html (NIST zero trust, TLS and authenticator assurance compliance)
- [primary] https://learn.microsoft.com/entra/standards/nist-authenticator-assurance-level-2 (NIST zero trust, TLS and authenticator assurance compliance)
- [primary] https://learn.microsoft.com/entra/identity-platform/app-resilience-continuous-access-evaluation (NIST zero trust, TLS and authenticator assurance compliance)
