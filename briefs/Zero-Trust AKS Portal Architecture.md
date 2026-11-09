Research Brief: Architecting a Zero-Trust, Identity-Federated Architecture for Internal AKS Applications
Core Research Question
1. Executive Summary & Context
Modern enterprise cloud environments frequently face the challenge of unifying user experience while maintaining strict microservice security. This research brief addresses the architecture required to deliver a single-entry portal for discovering and launching internal web applications hosted on Azure Kubernetes Service (AKS), while strictly adhering to Zero Trust Architecture (ZTA) principles.
Unlike traditional perimeter-based security models where an ingress gateway handles both authentication and authorization (leaving backend services open to implicit trust), this architecture enforces decentralized, application-level authorization. The portal acts as an identity bootstrap and routing hub, but individual downstream applications independently validate identity claims and enforce access controls.
Key Environmental Constraints
￼ Non-Internet Facing: All components operate strictly within private corporate networks (internal IP space).
￼ Single Namespace Scope: Security policies, ingress controls, and service boundaries are completely isolated to a dedicated Kubernetes namespace.
￼ Standards Compliance: Full alignment with NIST SP 800-207 (Zero Trust Architecture), NIST SP 800-52 Rev 2 (TLS Guidelines), and NIST SP 800-63B (Digital Identity Guidelines).
2. Scope and Boundaries
In-Scope
￼ Identity Provider Integration: Microsoft Entra ID integration via OAuth 2.0 / OpenID Connect (OIDC) using Authorization Code Flow with PKCE.
￼ Token Standard & Claim Injection: JSON Web Tokens (JWTs) bearing standard user attributes, security group memberships (⁠groups⁠), and fine-grained application roles (⁠roles⁠).
￼ Namespace Isolation: Ingress rules, TLS secret management, and network policies restricted exclusively to the target Kubernetes namespace.
￼ Zero Trust App Authorization: Independent JWT verification (signature, issuer, audience, roles) inside each micro-application.
￼ Transport Encryption: Strict internal TLS for ingress termination and Mutual TLS (mTLS) for pod-to-pod internal communications.
Out-of-Scope
￼ External public edge defenses (e.g., public Web Application Firewalls, internet-facing proxies).
￼ Multi-tenant cluster architectures spanning multiple production namespaces.
￼ Centralized proxy header-injection authentication patterns (e.g., relying solely on upstream ⁠X-Auth-Request-User⁠ headers).
3. Architectural Components & Data Flow
3.1 Identity Bootstrap & Session Propagation
￼ Centralized Authentication (Portal Launchpad): The internal portal (⁠portal.internal.company.local⁠) serves as the single entry point. Upon initial access, it initiates an OIDC flow against Microsoft Entra ID.
￼ Token Content Requirements: Entra ID must issue short-lived JWT Access Tokens containing identity claims (⁠sub⁠/⁠upn⁠), directory group IDs (⁠groups⁠), and assigned application roles (⁠roles⁠).
￼ Session Propagation: Browsers and client applications retain the Access Token and append it via standard ⁠Authorization: Bearer <JWT>⁠ headers on all API requests sent to downstream domain applications.
3.2 Ingress & Boundary Enforcement
￼ Namespace Isolation Principle: Ingress controllers operate with strict namespace affinity, ensuring ingress definitions, certificates, and routing configurations are isolated from neighboring cluster workloads.
￼ Internal TLS Termination: Ingress proxies terminate incoming TLS connections using private corporate Certificate Authority (CA) certificates while enforcing modern, secure cipher suites.
￼ Strict Host & Path Routing: Explicit host-based routing (⁠app1.internal.company.local⁠, ⁠app2.internal.company.local⁠) within the target namespace prevents unauthorized route interception or wildcard fallbacks.
3.3 Micro-Segmentation & Transport Security
￼ Zero Implicit Trust Network Policy: Enforce default-deny ingress and egress NetworkPolicies at the Kubernetes namespace boundary. Traffic flow is restricted strictly to authorized paths (e.g., ingress controller to workload pods).
￼ Mandatory mTLS: Pod-to-pod communications within the namespace strictly enforce Mutual TLS (mTLS) via a Service Mesh (e.g., Istio) utilizing short-lived SPIFFE/SPIRE identity certificates. Plaintext HTTP inside the cluster is prohibited.
4. Security & Compliance Alignment
4.1 NIST SP 800-207 (Zero Trust Architecture)
￼ Explicit Verification: Network location or ingress origin does not grant implicit access. Every application acts as its own Policy Enforcement Point (PEP).
￼ Decentralized Authorization: Micro-applications independently execute cryptographic signature validation using Entra ID public keys (JWKS), checking issuer (⁠iss⁠), audience (⁠aud⁠), expiration (⁠exp⁠), and matching role/group claims against local policy rules.
￼ Least Privilege Access: App Registrations in Entra ID enforce minimal, service-specific App Roles rather than broad directory-wide administrative rights.
4.2 NIST SP 800-52 Rev 2 (Guidelines for TLS Implementations)
￼ Cryptographic Standards: All ingress endpoints and in-cluster mTLS channels enforce TLS 1.3 or minimum TLS 1.2 with approved ephemeral key exchange algorithms (e.g., ECDHE) for forward secrecy.
￼ Automated Certificate Lifecycle: Short-lived internal certificates are dynamically issued, rotated, and managed through automated controllers (e.g., cert-manager, Service Mesh CA).
4.3 NIST SP 800-63B (Digital Identity Guidelines)
￼ Authenticator Assurance Level 2 (AAL2): Primary authentication via Microsoft Entra ID enforces Multi-Factor Authentication (MFA) prior to issuing identity assertions.
￼ Secure Token Handling: Applications treat access tokens as non-transferable bearer credentials, enforcing strict expiration boundaries and rejecting malformed or expired tokens immediately.
5. Evaluation Criteria & Trade-Off Analysis
5.1 Security posture vs. Application Latency
￼ Trade-Off: Local JWT validation requires applications to periodically fetch public keys (JWKS) and perform cryptographic signature checks on every request.
￼ Best Practice: Implement robust, non-blocking JWKS caching algorithms within application runtimes to minimize validation latency while maintaining security freshness.
5.2 Operational Overhead vs. Decentralized Governance
￼ Trade-Off: Enforcing authorization inside applications increases application codebase responsibilities and requires standardizing authentication libraries across development teams.
￼ Best Practice: Provide standard middleware libraries or sidecar proxies (e.g., Envoy ⁠RequestAuthentication⁠) across the development organization to streamline JWT verification while keeping business logic decoupled.
5.3 Centralized Management vs. Zero Trust Resiliency
￼ Trade-Off: While central proxies simplifies management, decentralized zero-trust authorization ensures that a breach or misconfiguration at the ingress proxy level does not compromise downstream applications.
