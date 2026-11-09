# Verification run: all six topic groups

Run: deep-research workflow wf_4f283622-cb6 (variant: 6 angles, fetch budget 30, round-robin claim selection across angles, max 48).
Stats: {"angles": 6, "sourcesFetched": 34, "claimsExtracted": 168, "claimsVerified": 48, "confirmed": 44, "killed": 4, "unverified": 0, "afterSynthesis": 20, "urlDupes": 0, "budgetDropped": 2, "agentCalls": 186}

## Summary

The verification confirms the main design: give each trust boundary its own Entra app registration, manage registrations with the hashicorp/azuread provider, use v2.0 access tokens and validate aud against the appId, and authenticate confidential clients on AKS with federated credentials instead of secrets. The least-privileged Graph permission for the Terraform identity is Application.ReadWrite.OwnedBy, and the identity must be an owner of every registration it manages. OwnedBy still reads every app in the tenant, and it does not cover group-to-app-role assignments or admin-consent grants. Those need AppRoleAssignment.ReadWrite.All or Directory.ReadWrite.All (per the provider docs). Both are highly privileged, and Microsoft warns that AppRoleAssignment.ReadWrite.All lets an app grant privileges to itself. Several Entra limits are confirmed: federated credentials cap at 20 per app, require an exact subject match with no wildcards, and take a single audience. Assigning groups to app roles needs Entra ID P1/P2 and does not cascade to nested groups. Single sign-on (SSO) relies on the Entra session cookie, and single sign-out needs a front-channel logout URL on every app and only works best-effort. Several items remain unverified and are listed under caveats and open questions: the PEP definition, the AKS and network items (Istio PILOT_JWT_ENABLE_REMOTE_JWKS, the AzureActiveDirectory service tag, the internal load balancer annotation, cert-manager and trust-manager), and the IETF and RFC items (BFF draft, RFC 9068, RFC 6750, RFC 6762).

## F1 (high, vote 3-0 (merged claims 0,5,6,10,11,23))

Least-privilege Terraform identity: Application.ReadWrite.OwnedBy is an application-only permission and needs admin consent. It can create applications and service principals and fully manage only the ones it owns, including updating secrets. It cannot update apps it does not own, but it can still list and read every application and service principal in the tenant (GET /applications, /servicePrincipals). Application.ReadWrite.All covers create, read, update and delete on all applications and service principals, and app role assignments except Graph-exposed ones. It does not cover delegated permission grants, and Microsoft warns that permissions which manage credentials let an app act as other entities. The azuread provider docs say azuread_application needs OwnedBy or ReadWrite.All when Terraform runs as a service principal. With OwnedBy, the Terraform principal should be in the application's owners list. User.Read.All may be needed when user principals are owners. When Terraform runs as a user, the docs name Application Administrator or Global Administrator and do not mention Cloud Application Administrator. Guidance: put the Terraform service principal in owners on every azuread_application. Add it as an owner of each existing manual registration before running terraform import.

**Evidence:** Graph reference: 'It cannot update any apps that it is not an owner of'; 'allows the same operations as Application.ReadWrite.All but only on applications and service principals that the calling app is an owner of'; 'allows an app to call GET /applications and GET /servicePrincipals ... to list all'. Application.ReadWrite.All: 'Does not allow management of delegated permission grants.' Provider docs, lines 15-21. Merged claims 0, 5, 6, 10, 11 and 23, all voted 3-0.

**Sources:**
- https://learn.microsoft.com/graph/permissions-reference
- https://learn.microsoft.com/en-au/graph/permissions-overview
- https://raw.githubusercontent.com/hashicorp/terraform-provider-azuread/main/docs/resources/application.md
- https://www.pulumi.com/registry/packages/azuread/api-docs/application/

## F2 (high, vote 3-0 (merged claims 17,22,32))

Group-to-app-role assignment from Terraform needs a highly privileged permission. When it runs as a service principal, azuread_app_role_assignment needs one of these: AppRoleAssignment.ReadWrite.All plus Application.Read.All, AppRoleAssignment.ReadWrite.All plus Directory.Read.All, Application.ReadWrite.All, or Directory.ReadWrite.All. Microsoft warns that AppRoleAssignment.ReadWrite.All can grant application permissions to any API, Microsoft Graph included, and so lets an app grant additional privileges to itself, other apps or any user. The resource supports users, groups and service principals as principal_object_id. Mitigation (inference): run this part from a separate, tightly controlled Terraform identity or pipeline stage, not from the per-app pipelines.

**Evidence:** Graph reference: 'Permissions that allow granting authorization, such as AppRoleAssignment.ReadWrite.All, allow an application to grant additional privileges to itself, other applications, or any user.' The provider docs list the four permission sets and say 'Supported object types are Users, Groups or Service Principals.' Merged claims 17, 22 and 32, all voted 3-0.

**Sources:**
- https://learn.microsoft.com/graph/permissions-reference
- https://raw.githubusercontent.com/hashicorp/terraform-provider-azuread/main/docs/resources/app_role_assignment.md
- https://www.pulumi.com/registry/packages/azuread/api-docs/approleassignment/

## F3 (medium, vote 2-1 (claim 38))

Admin consent from Terraform: the azuread provider docs say azuread_service_principal_delegated_permission_grant needs the Directory.ReadWrite.All application role when it runs as a service principal. This wording is the same in v2.53.1, v3.0.0 and main. The docs do not mention DelegatedPermissionGrant.ReadWrite.All. Graph may accept DelegatedPermissionGrant.ReadWrite.All as a narrower permission for creating an oauth2PermissionGrant, but that comes from the verifier's memory and was not checked in this run. So the report should say 'the provider documents Directory.ReadWrite.All', not 'Graph requires it'.

**Evidence:** Provider docs: 'When authenticated with a service principal, this resource requires the following application role: Directory.ReadWrite.All.' The vote was split 2-1. The related claim that a user principal needs Global Administrator was refuted 0-3.

**Sources:**
- https://raw.githubusercontent.com/hashicorp/terraform-provider-azuread/main/docs/resources/service_principal_delegated_permission_grant.md
- https://www.pulumi.com/registry/packages/azuread@5.x/api-docs/serviceprincipaldelegatedpermissiongrant/

## F4 (high, vote 3-0 (claim 16))

In azuread_application, every app_role block needs an explicit id that is a valid UUID. The provider docs suggest generating it with a random_uuid resource and expose an app_role_ids output. Inference: the IDs stay stable across applies as long as the Terraform state persists. A hard-coded literal UUID gives the same stability without depending on state. Recommended: hard-code role UUIDs, or keep them in random_uuid resources protected with lifecycle prevent_destroy.

**Evidence:** Provider docs, line 282: 'id - (Required) The unique identifier of the app role. Must be a valid UUID.' Line 284 is the random_uuid tip. That IDs stay stable across applies is inference and is not stated in the docs.

**Sources:**
- https://raw.githubusercontent.com/hashicorp/terraform-provider-azuread/main/docs/resources/application.md
- https://www.pulumi.com/registry/packages/azuread/api-docs/application/

## F5 (high, vote 3-0 (claim 8))

A resource app (web API) with custom identifier URIs, meaning anything other than api://{appId} or api://{tenantId}/{appId}, should use v2.0 access tokens. In Graph this is requestedAccessTokenVersion = 2; in Terraform it is api.requested_access_token_version = 2. After the switch, the API's audience validation should accept only its appId. Microsoft says to confirm first that the API can handle v2.0 claims.

**Evidence:** Microsoft: 'ensure the application's audience validation logic is modified to only accept its appId.' Page dated 2026-10.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/security-best-practices-for-app-registration

## F6 (high, vote 3-0 (merged claims 32,33,39))

Licensing and roles for group-to-app-role assignment: group-based assignment needs Microsoft Entra ID P1 or P2. A group assignment does not cascade to nested groups, so only direct members get access. The minimum roles that can assign users or groups to an enterprise app are Cloud Application Administrator, Application Administrator, User Administrator and owner of the service principal. Higher roles such as Global Administrator also work; that part is inference. The azuread provider docs say nothing about licensing.

**Evidence:** Microsoft: 'Group-based assignment requires Microsoft Entra ID P1 or P2 edition. Nested group memberships aren't currently supported.' The Prerequisites section lists the four roles. Merged claims 33, 39 and 32.

**Sources:**
- https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal
- https://raw.githubusercontent.com/hashicorp/terraform-provider-azuread/main/docs/resources/app_role_assignment.md

## F7 (high, vote 3-0 (claim 2))

Credential order of preference for an app registration: (1) a managed identity used as a federated credential, which Microsoft strongly recommends; (2) a federated identity from another trusted platform; (3) a certificate; (4) never a password secret. App management policies can restrict or block secrets.

**Evidence:** Microsoft: 'Use a managed identity as a credential whenever possible... Don't use password credentials, also known as secrets.' Page updated 2026-10-02.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/security-best-practices-for-app-registration

## F8 (high, vote 3-0 (merged claims 1,7,12))

Limits on federated identity credentials (FICs) for AKS Workload ID: an application or user-assigned managed identity can hold at most 20 FICs. The subject must exactly match the external token's sub, for example system:serviceaccount:<ns>:<sa>. No FIC property accepts wildcards. A wrong subject is accepted when the FIC is created and only fails at token exchange. Each FIC takes exactly one audience; api://AzureADTokenExchange is the recommended value, and the error table says it is the only one currently supported. Flexible FICs (claimsMatchingExpression) cover only GitHub, GitLab and Terraform Cloud, not AKS. So each cluster issuer and service-account pair needs its own FIC, and the 20 per app cap applies. Guidance: use one service account per app in the single namespace. Create the FIC with azuread_application_federated_identity_credential, setting issuer to the cluster OIDC issuer URL and subject to system:serviceaccount:<ns>:<sa>.

**Evidence:** Microsoft: 'A maximum of 20 federated identity credentials can be added'; 'Wildcard characters aren't supported in any federated identity credential property value'; 'You must add a single audience value'. The page is primary and current, updated 2026-06. The 20 limit was also confirmed on the flexible FIC page. Merged claims 1, 7 and 12. The azuread_application_federated_identity_credential resource docs themselves were not fetched.

**Sources:**
- https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations

## F9 (high, vote 3-0 (merged claims 18,24,28,34))

A secretless BFF / web app works through Microsoft.Identity.Web. A web app set up with AddMicrosoftIdentityWebAppAuthentication(...).EnableTokenAcquisitionToCallDownstreamApi() can take a federated credential in ClientCredentials in place of a secret. Two SourceTypes apply. SignedAssertionFromManagedIdentity is recommended for Azure production; it accepts only user-assigned managed identities, and its FIC subject is the managed identity's principal ID with issuer login.microsoftonline.com/{tenant}/v2.0. SignedAssertionFilePath reads a signed assertion from a file 'for Kubernetes workload identity'; this is the projected service account token. For AKS pods, Microsoft.Identity.Web.Certificateless offers AzureIdentityForKubernetesClientAssertion, which reads AZURE_FEDERATED_TOKEN_FILE and returns it as the client assertion. In plain MSAL.NET, a callback goes to ConfidentialClientApplicationBuilder.WithClientAssertion(Func<AssertionRequestOptions,Task<string>>). MSAL calls it for each token request, and caching the assertion is the implementer's job. So the client credential of a user-facing auth-code web app can be a federated credential.

**Evidence:** The credentials overview shows the web-app sign-in plus downstream-API sample with CredentialSource.SignedAssertionFromManagedIdentity and lists 'SignedAssertionFilePath | Federated | ... (for Kubernetes workload identity)'. The MSAL article says 'To acquire a federated token in a Azure Kubernetes cluster, use AzureIdentityForKubernetesClientAssertion.' Merged claims 18, 24, 28 and 34.

**Sources:**
- https://learn.microsoft.com/entra/msidweb/authentication/credentials-overview
- https://learn.microsoft.com/en-us/entra/msal/dotnet/acquiring-tokens/web-apps-apis/workload-identity-federation
- https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-config-app-trust-managed-identity
- https://github.com/AzureAD/microsoft-identity-web (src/Microsoft.Identity.Web.Certificateless/AzureIdentityForKubernetesClientAssertion.cs)

## F10 (medium, vote 2-1 (claim 40))

The MSAL.NET workload identity federation article shows only a client-credentials call (AcquireTokenForClient). It never shows or states that the assertion is used in an authorization-code (BFF) flow. The Microsoft.Identity.Web credentials overview does show the web-app sign-in sample, so support for the auth-code flow rests on that page. For a pod using SignedAssertionFilePath in an interactive web app, it is still inference: no doc shows that combination end to end, no minimum package version is documented, and no default file path is documented.

**Evidence:** The page's only token-acquisition example is 'var result = await app.AcquireTokenForClient(scope).ExecuteAsync();'. The vote was split 2-1.

**Sources:**
- https://learn.microsoft.com/en-us/entra/msal/dotnet/acquiring-tokens/web-apps-apis/workload-identity-federation

## F11 (high, vote 3-0 (merged claims 13,29,35))

How SSO works across separate app registrations: when the user first authenticates, Entra sets a session cookie on its own domain, and other apps reuse that session. prompt=none signs in silently and returns an error instead of a prompt when SSO cannot complete (no user signed in, the hinted user not signed in, or several users and no hint). It should be paired with login_hint. ssoSilent in MSAL.js uses a hidden iframe, so it fails with AADSTS50058 in browsers that block third-party cookies, such as Safari. The fallback is loginRedirect or loginPopup, sometimes with prompt=none. A server-side BFF that uses full-page redirects avoids the iframe problem; that point is inference. Picking an account, consent on first use and Conditional Access scoped to a particular app can still cause prompts.

**Evidence:** Microsoft: 'a session cookie is set on the Microsoft Entra domain... MSAL.js relies on this session cookie to provide SSO ... between different applications'; 'If the request can't be completed silently via single sign-on, the Microsoft identity platform returns an error.' Merged claims 13, 29 and 35.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-sso
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc

## F12 (high, vote 3-0 (merged claims 19,25))

Limits on single sign-out: redirecting to end_session_endpoint ends the session only for that application. For single sign-out, each app registration has to set its one front-channel logout URL (web.logoutUrl). Entra then sends an HTTP GET to the front-channel logout URL of every app the user is signed in to. Each app must clear its session and return 200. Because delivery goes through browser iframes, it is best-effort when third-party cookies are blocked; that point is inference. The feature covers web and SPA apps in the same tenant.

**Evidence:** Microsoft: 'the Microsoft identity platform ends the user session for this application. However, the user may still be signed in to other applications'; 'Each application has one front channel logout URL.' Merged claims 19 and 25.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc

## F13 (medium, vote 3-0 (claim 41))

My Apps as a launchpad: an enterprise app appears in a user's My Apps portal only if it is marked visible and the user, or a group they belong to, is assigned to it. A visible app with no assignments does not show. So My Apps tiles for internal apps depend on app role assignments, and group-based assignment needs P1/P2. The source does not say whether a link to a non-internet-facing app works from My Apps. Inference: the tile is only a link, and the user's browser needs network reach to the internal app.

**Evidence:** Microsoft: 'applications still don't appear in the My Apps portal if they don't yet have users or groups assigned to it.' This rests on one primary source, last updated in 2024.

**Sources:**
- https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/myapps-overview

## F14 (high, vote 3-0 (claim 3))

Prerequisites for AKS FQDN egress filtering: it is an Advanced Container Networking Services (ACNS) Container Network Security feature. It requires Azure CNI Powered by Cilium and Kubernetes 1.29 or later, and ACNS security must be enabled. ACNS is a paid add-on. Known limits: Kubernetes service names are not supported, cluster-wide policies use CiliumClusterwideNetworkPolicy, and Alpine/musl images can have DNS search-domain problems.

**Evidence:** Microsoft: 'Azure CNI Powered by Cilium and Kubernetes version 1.29 or greater is required in order to use Container Network security features of Advanced Container Networking Services.' The page was updated 2026-08. The overview page confirms Cilium only. A separate claim about licensing wording was refuted 0-3, so the exact licensing terms rest only on the pricing page.

**Sources:**
- https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts
- https://learn.microsoft.com/en-us/azure/aks/advanced-container-networking-services-overview

## F15 (medium, vote 2-1 (claim 14))

Azure Firewall alternative: Azure Firewall offers an AzureKubernetesService FQDN tag. It holds all the FQDNs in AKS's required outbound rules, is updated automatically, and is used in application rules on ports 80 and 443. The required-rules page lists login.microsoftonline.com:443 for Entra authentication and workload identity. That suggests the tag covers it, but this is inference. Neither page mentions graph.microsoft.com or the AzureActiveDirectory service tag. Guidance (inference): add explicit application rules for login.microsoftonline.com and graph.microsoft.com instead of relying on the AKS tag for app traffic.

**Evidence:** Microsoft: 'The FQDN tag contains all the FQDNs listed in outbound network and FQDN rules for AKS clusters and is automatically updated.' A text search found no AzureActiveDirectory or graph.microsoft.com. The vote was split 2-1.

**Sources:**
- https://learn.microsoft.com/azure/aks/limit-egress-traffic
- https://learn.microsoft.com/en-us/azure/aks/outbound-rules-control-egress

## F16 (high, vote 3-0 (merged claims 20,26))

Envoy jwt_authn remote JWKS: when RemoteJwks.cache_duration is not set, the cache lasts 10 minutes (DefaultCacheExpirationSec=600 in source). Without async_fetch, each worker thread fetches the JWKS on demand, and the first requests wait until the fetch finishes. With async_fetch, the main thread fetches the keys before the listener is activated (unless fast_listener=true), all workers share them, and the main thread refetches when the cache expires. This applies only when Envoy fetches the JWKS itself. Under Istio, istiod normally resolves jwksUri and inlines the keys unless PILOT_JWT_ENABLE_REMOTE_JWKS is enabled; that statement is the verifier's background knowledge and was not checked against Istio docs. Envoy's behaviour on an unknown kid was not verified.

**Evidence:** Proto: 'If not specified, default cache duration is 10 minutes.'; 'Fetch Jwks asynchronously in the main thread before the listener is activated.' The Envoy source code confirms both. Merged claims 20 and 26.

**Sources:**
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/jwt_authn_filter
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/http/jwt_authn/v3/config.proto
- https://github.com/envoyproxy/envoy (source/extensions/filters/http/jwt_authn/jwks_async_fetcher.cc)

## F17 (high, vote 3-0 (merged claims 30,36,42))

Continuous Access Evaluation (CAE) and claims challenges for custom APIs: apps that use CAE or Conditional Access authentication context must handle claims challenges. A client gets no claims challenges and no CAE tokens until it declares the cp1 capability. In Microsoft.Identity.Web this is AzureAd:ClientCapabilities ['cp1']; in MSAL it is WithClientCapabilities. A custom API sees cp1 only if its own registration requests xms_cc as an optional access-token claim, and the claim appears only when the client sent xms_cc. A challenge must be HTTP 401 with WWW-Authenticate: Bearer, plus authorization_uri, error=insufficient_claims and a base64 claims value. Clients without cp1 should get a plain error; Microsoft's sample returns 403.

**Evidence:** Microsoft: 'An application won't receive claims challenges ... unless it declares it's ready to handle them with the cp1 capability'; 'the resource application ... must request xms_cc as an optional claim'; 'HTTP Status Code: Must be 401 Unauthorized.' Merged claims 30, 36 and 42. This rests on one primary page, cross-checked against the entra-docs source. Whether CAE revocation events actually reach custom APIs was not verified.

**Sources:**
- https://learn.microsoft.com/entra/identity-platform/claims-challenge

## F18 (high, vote 3-0 (merged claims 4,9))

PyJWT PyJWKClient defaults: cache_keys=False, max_cached_keys=16, cache_jwk_set=True, lifespan=300 s, timeout=30 and cooldown_duration=30. When a token's kid is not in the cached set, get_signing_key refreshes once and retries, but only if 30 s have passed since the last successful fetch. Otherwise, or if there is still no match after the refresh, it raises PyJWKClientError. The cooldown applies only when the JWK Set cache is enabled. These defaults hold only for recent PyJWT versions, since cooldown_duration is new.

**Evidence:** Docs signature: 'PyJWKClient(uri, cache_keys=False, max_cached_keys=16, cache_jwk_set=True, lifespan=300, ..., cooldown_duration=30)'. Docstring: 'the set is refreshed from the endpoint and the lookup is retried once when the refresh cooldown permits it'. The source code agrees. Merged claims 4 and 9.

**Sources:**
- https://pyjwt.readthedocs.io/en/stable/api.html
- https://raw.githubusercontent.com/jpadilla/pyjwt/master/jwt/jwks_client.py

## F19 (high, vote 3-0 (merged claims 15,21,27))

Gateway API rules for a single namespace: a Listener's allowedRoutes.namespaces defaults to from: Same; the alternatives are All and Selector. A certificateRefs entry pointing to a Secret in another namespace is invalid unless a ReferenceGrant in that namespace allows Gateway-to-Secret references. Otherwise ResolvedRefs is False with reason RefNotPermitted. An HTTPRoute attaches only if its hostnames and the Listener's intersect, when both set hostnames. *.example.com matches subdomains as a suffix but not example.com itself. With the Gateway, routes and TLS secret all in the one app namespace, no ReferenceGrant is needed; that point is inference.

**Evidence:** Spec: '(default { from:Same })'; 'References to a resource in different namespace are invalid UNLESS there is a ReferenceGrant in the target namespace'; 'Hostnames that are prefixed with a wildcard label (*.) are interpreted as a suffix match.' Merged claims 15, 21 and 27.

**Sources:**
- https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- https://raw.githubusercontent.com/kubernetes-sigs/gateway-api/main/apis/v1/gateway_types.go

## F20 (high, vote 3-0 (merged claims 31,37,43))

NIST SP 800-207 (final, 2020; still current) sets out exactly seven tenets. Tenet 2: network location alone does not imply trust, so requests from inside the network, such as an internal-only AKS app behind an internal load balancer, must meet the same requirements. Tenet 3: access is granted per session with least privilege, and authentication and authorization to one resource do not automatically grant access to another. Section 3.1: the policy decision point (PDP) is made up of the policy engine (PE), which makes and logs the grant or deny decision, and the policy administrator (PA), which carries it out by commanding policy enforcement points (PEPs) and issuing session-specific tokens or credentials. An implementation may merge the PE and PA. Mapping Entra to the PE/PA and Istio/Envoy to the PEP, and reading tenet 3 as support for one audience per app, is inference: NIST is technology-neutral.

**Evidence:** NIST: 'Network location alone does not imply trust'; 'authentication and authorization to one resource will not automatically grant access to a different resource'; 'the policy decision point (PDP) is broken down into two logical components'. Checked against the full PDF text. Merged claims 31, 37 and 43.

**Sources:**
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

## Refuted

- (0-3) Advanced Container Networking Services, which provides FQDN filtering, is a paid offering and needs no separate licence beyond its own pricing. If ACNS security is disabled, FQDN and L7 policies are blocked. - https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts
- (1-2) When the provider authenticates as a user, the resource needs the Application Administrator or Global Administrator directory role. - https://www.pulumi.com/registry/packages/azuread/api-docs/approleassignment/
- (0-3) Application permissions (app roles) require admin consent, and only the Privileged Role Administrator and Global Administrator roles can consent to them. A Terraform identity's Graph application permissions therefore need consent from one of those roles. - https://learn.microsoft.com/en-au/graph/permissions-overview
- (0-3) When it authenticates as a user principal, the resource requires the Global Administrator directory role. - https://www.pulumi.com/registry/packages/azuread@5.x/api-docs/serviceprincipaldelegatedpermissiongrant/

## Caveats

Coverage is uneven. Many items in the brief had no claim that survived verification, so the report must list them as unverified rather than confirmed: (a) that destroying and recreating an azuread_application issues a new client ID; (b) the docs for azuread_application_federated_identity_credential and required_resource_access, and the identifier_uris and web redirect_uris syntax; (c) how app_role_assignment_required changes token issuance; (d) DelegatedPermissionGrant.ReadWrite.All as a narrower option than Directory.ReadWrite.All; (e) Istio RequestAuthentication fetching via istiod versus Envoy, PILOT_JWT_ENABLE_REMOTE_JWKS, and Envoy's behaviour on an unknown kid; (f) the AzureActiveDirectory service tag; (g) the IETF OAuth 2.0 for Browser-Based Apps BFF recommendation and its status, RFC 9068 and RFC 6750; (h) the service.beta.kubernetes.io/azure-load-balancer-internal annotation; (i) cert-manager private CA issuers and trust-manager; (j) .local reserved for mDNS (RFC 6762); (k) the NIST PEP definition itself; (l) sharing one registration with per-app prefixed roles versus one per trust boundary, which is a design inference from NIST tenet 3 and Microsoft guidance, not a documented rule. Weak points: three claims had split votes (Firewall FQDN tag, delegated-grant permission, MSAL auth-code example). Some azuread claims were cited from Pulumi mirrors, though each was re-checked against HashiCorp docs on main. Several findings rest on a single Microsoft Learn page. Time sensitivity: the provider permission lists, FIC limits (flexible FICs are in preview), ACNS prerequisites and pricing, and the PyJWT defaults (cooldown_duration is recent) all change over time. Refuted claims: that only Privileged Role Administrator and Global Administrator can consent to application permissions (0-3); that the delegated-grant resource needs Global Administrator when run as a user (0-3); that azuread_app_role_assignment run as a user needs Application Administrator or Global Administrator (1-2); and a licensing wording about ACNS (0-3). The report should not repeat any of these as fact.

## Open questions

- Does Istio's AKS service mesh add-on inline the JWKS through istiod, or does Envoy fetch it remotely? If Envoy fetches it, which PILOT_JWT_ENABLE_REMOTE_JWKS setting applies, and how fast does each path pick up an Entra signing-key rollover or an unknown kid?
- Is there an end-to-end Microsoft-documented sample of an interactive auth-code web app (BFF) on AKS that uses SignedAssertionFilePath or AzureIdentityForKubernetesClientAssertion as its only client credential, and what is the minimum Microsoft.Identity.Web version?
- What is the narrowest Graph permission set that lets one Terraform identity manage registrations (OwnedBy), group-to-role assignments and admin consent, without AppRoleAssignment.ReadWrite.All or Directory.ReadWrite.All? For example, does DelegatedPermissionGrant.ReadWrite.All work with the azuread provider in practice?
- Does the AzureKubernetesService FQDN tag, or the AzureActiveDirectory service tag, cover graph.microsoft.com and login.microsoftonline.com for application workload traffic, or are explicit Azure Firewall application rules needed?

## Sources fetched

- [secondary] https://www.pulumi.com/registry/packages/azuread/api-docs/application/ (Terraform azuread app registration automation)
- [secondary] https://www.pulumi.com/registry/packages/azuread/api-docs/approleassignment/ (Terraform azuread app registration automation)
- [secondary] https://www.pulumi.com/registry/packages/azuread@5.x/api-docs/serviceprincipaldelegatedpermissiongrant/ (Terraform azuread app registration automation)
- [blog] https://oneuptime.com/blog/post/2026-02-23-how-to-create-azure-active-directory-applications-in-terraform/markdown (Terraform azuread app registration automation)
- [blog] https://dev.to/danquack/azuread-37-dynamic-credentials-with-flexible-federated-identity-4ji9 (Terraform azuread app registration automation)
- [forum] https://www.github.com/hashicorp/terraform-provider-azuread/issues/1352 (Terraform azuread app registration automation)
- [primary] https://learn.microsoft.com/graph/permissions-reference (Graph permissions and Entra roles for Terraform identity)
- [primary] https://learn.microsoft.com/en-au/graph/permissions-overview (Graph permissions and Entra roles for Terraform identity)
- [primary] https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal (Graph permissions and Entra roles for Terraform identity)
- [primary] https://learn.microsoft.com/entra/identity/enterprise-apps/what-is-access-management (Graph permissions and Entra roles for Terraform identity)
- [primary] https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/application (Graph permissions and Entra roles for Terraform identity)
- [secondary] https://www.pulumi.com/registry/packages/azuread/api-docs/serviceprincipaldelegatedpermissiongrant/ (Graph permissions and Entra roles for Terraform identity)
- [primary] https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations (Workload ID federated credential for web app auth code flow)
- [primary] https://learn.microsoft.com/entra/msidweb/authentication/credentials-overview (Workload ID federated credential for web app auth code flow)
- [primary] https://github.com/MicrosoftDocs/microsoft-authentication-library-dotnet/blob/main/msal-dotnet-articles/acquiring-tokens/web-apps-apis/workload-identity-federation.md (Workload ID federated credential for web app auth code flow)
- [primary] https://learn.microsoft.com/entra/msidweb/authentication/certificateless (Workload ID federated credential for web app auth code flow)
- [primary] https://learn.microsoft.com/azure/aks/workload-identity-overview (Workload ID federated credential for web app auth code flow)
- [primary] https://learn.microsoft.com/entra/workload-id/workload-identities-flexible-federated-identity-credentials (Workload ID federated credential for web app auth code flow)
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/security-best-practices-for-app-registration (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/entra/identity-platform/msal-js-sso (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/myapps-overview (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/application-properties (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/security/zero-trust/develop/app-registration (Entra SSO, My Apps and sign-out limits)
- [primary] https://learn.microsoft.com/en-us/azure/aks/container-network-security-fqdn-filtering-concepts (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://learn.microsoft.com/azure/aks/limit-egress-traffic (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/jwt_authn_filter (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://learn.microsoft.com/entra/identity-platform/claims-challenge (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://cloud.google.com/service-mesh/docs/security/configuring-remote-jwks-request-authentication (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://learn.microsoft.com/entra/identity-platform/app-resilience-continuous-access-evaluation (AKS egress FQDN filtering, Istio JWKS, CAE)
- [primary] https://pyjwt.readthedocs.io/en/stable/api.html (Standards and K8s networking/PKI references)
- [primary] https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/ (Standards and K8s networking/PKI references)
- [primary] https://csrc.nist.gov/pubs/sp/800/207/final (Standards and K8s networking/PKI references)
- [primary] https://learn.microsoft.com/azure/aks/internal-lb (Standards and K8s networking/PKI references)

## Verification log

- "Application.ReadWrite.OwnedBy (applicati…": 3-0 ✓
- "An application or user-assigned managed…": 3-0 ✓
- "Microsoft strongly recommends using a ma…": 3-0 ✓
- "AKS FQDN filtering (ACNS Container Netwo…": 3-0 ✓
- "The PyJWKClient constructor defaults are…": 3-0 ✓
- "The azuread Application resource needs e…": 3-0 ✓
- "Application.ReadWrite.OwnedBy allows the…": 3-0 ✓
- "The FIC subject must exactly match the e…": 3-0 ✓
- "Resource apps (web APIs) with custom ide…": 3-0 ✓
- "Advanced Container Networking Services,…": 0-3 ✗
- "When the cached JWK Set has no key match…": 3-0 ✓
- "When authenticating with directory roles…": 3-0 ✓
- "Application.ReadWrite.All covers create,…": 3-0 ✓
- "A federated identity credential takes ex…": 3-0 ✓
- "prompt=none performs silent sign-in usin…": 3-0 ✓
- "Azure Firewall offers an AzureKubernetes…": 2-1 ✓
- "A Listener's allowedRoutes.namespaces co…": 3-0 ✓
- "Each app_role block needs an explicit id…": 3-0 ✓
- "AppRoleAssignment.ReadWrite.All can gran…": 3-0 ✓
- "Microsoft.Identity.Web supports a Source…": 3-0 ✓
- "Redirecting to end_session_endpoint ends…": 3-0 ✓
- "In Envoy's jwt_authn filter, remote JWKS…": 3-0 ✓
- "A Gateway Listener's TLS certificateRefs…": 3-0 ✓
- "When the provider authenticates as a ser…": 3-0 ✓
- "Application.ReadWrite.OwnedBy limits an…": 3-0 ✓
- "A web app configured with AddMicrosoftId…": 3-0 ✓
- "Each application registration has exactl…": 3-0 ✓
- "Without async_fetch, Envoy fetches the J…": 3-0 ✓
- "An HTTPRoute attaches to a Listener only…": 3-0 ✓
- "When the provider authenticates as a use…": 1-2 ✗
- "Application permissions (app roles) requ…": 0-3 ✗
- "MSAL.NET supports secretless confidentia…": 3-0 ✓
- "SSO between different apps (different ap…": 3-0 ✓
- "A claims challenge from an API (custom w…": 3-0 ✓
- "NIST SP 800-207 defines exactly seven ze…": 3-0 ✓
- "The resource can assign app roles to use…": 3-0 ✓
- "Assigning groups to an application (app…": 3-0 ✓
- "For AKS, Microsoft.Identity.Web provides…": 3-0 ✓
- "ssoSilent uses a hidden iframe, so it fa…": 3-0 ✓
- "Apps that use Continuous Access Evaluati…": 3-0 ✓
- "Tenet 3: access is granted per session w…": 3-0 ✓
- "The azuread delegated permission grant r…": 2-1 ✓
- "The roles that can assign users/groups t…": 3-0 ✓
- "The page's only code example shows a cli…": 2-1 ✓
- "An enterprise application appears in a u…": 3-0 ✓
- "A web API can only see whether a client…": 3-0 ✓
- "The policy decision point (PDP) is split…": 3-0 ✓
- "When it authenticates as a user principa…": 0-3 ✗
