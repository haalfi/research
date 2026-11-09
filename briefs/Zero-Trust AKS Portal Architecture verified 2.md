Second verification follow-up for "Zero-Trust AKS Portal Architecture".
Requested by the user ("yes, go ahead with group 1 and the test plan") after the open items of
reports/Zero-Trust AKS Portal Architecture verified.md were sorted into three groups:
group 1 = closable by reading a known primary source, group 2 = closable only by a sandbox test,
group 3 = closable only by Microsoft. This run covers group 1 and writes a test plan for group 2.

Scope agreed in conversation:

Group 1 (targeted fetch of named primary sources, then 3-vote adversarial verification):
1. AKS internal load balancer annotation (service.beta.kubernetes.io/azure-load-balancer-internal) and related annotations.
2. RFC 6762: is .local reserved for mDNS, and what names does it recommend for private networks.
3. RFC 9068: JWT access token profile (typ, required claims, audience validation, roles/groups claims).
4. RFC 6750: bearer token usage (Authorization header, error codes, TLS, token in URL).
5. IETF OAuth 2.0 for Browser-Based Apps: current status and the BFF recommendation.
6. cert-manager private CA issuers (CA issuer, Issuer vs ClusterIssuer scope) and trust-manager.
7. hashicorp/azuread provider syntax: application_federated_identity_credential, application optional_claims,
   web redirect_uris and logout_url, required_resource_access, sign_in_audience.
8. Istio RequestAuthentication jwksUri: fetched by istiod and inlined, or by Envoy (PILOT_JWT_ENABLE_REMOTE_JWKS).
Also documentation checks for items otherwise in groups 2 and 3, where docs may partly answer:
9. Effect of appRoleAssignmentRequired ("Assignment required") on token issuance.
10. Least-privileged Graph permission to create an oAuth2PermissionGrant (DelegatedPermissionGrant.ReadWrite.All?).
11. AzureActiveDirectory service tag and Azure Firewall FQDN tags: coverage of login.microsoftonline.com / graph.microsoft.com.
12. Continuous Access Evaluation: which resource providers support it; whether custom APIs receive revocation events.

Group 2 (sandbox tests, written as a test plan, not executed in this session):
recreated registration gets new client ID; "Assignment required" blocks unassigned users;
pod workload-identity token as the only credential for interactive sign-in (Microsoft.Identity.Web SignedAssertionFilePath);
DelegatedPermissionGrant.ReadWrite.All sufficient for azuread delegated grant resource;
AKS Istio add-on JWKS handling via istioctl proxy-config.
