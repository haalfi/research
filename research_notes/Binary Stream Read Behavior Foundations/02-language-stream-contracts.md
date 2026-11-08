# Track 02: Stream abstraction contracts in programming languages and runtimes

Retrieved 2026-11-08. Every source below was fetched as full text (raw source or the normative document) into
`/tmp/claude-0/-home-user-research/f4e62a10-8522-5595-9751-6bbd94c2238a/scratchpad/dl/language-stream-contracts/`.
Where a doc comment is the contract, it was read in the source file that ships with the language.

## Sources consulted (access status)

| # | Source | Type | Access |
|---|---|---|---|
| S1 | ISO/IEC 9899:201x Committee Draft N1570 (C11), 12 Apr 2011, §7.21.2, §7.21.7.1, §7.21.8.1, §7.21.10.2-3 | normative (final draft; the published ISO text is paywalled and was not read) | full text (open-std.org PDF) |
| S2 | POSIX.1-2024 (IEEE Std 1003.1-2024), `read()` incl. RATIONALE | normative | full text (pubs.opengroup.org) |
| S3 | Go `src/io/io.go` (master): `Reader`, `EOF`, `ErrUnexpectedEOF`, `ReadAtLeast`, `ReadFull` | implementation-doc (language std-lib contract) | full text (raw.githubusercontent) |
| S4 | Go `src/encoding/binary/binary.go`, `src/compress/gzip/gunzip.go` (master) | implementation-doc | full text |
| S5 | Rust `library/std/src/io/mod.rs` and `io/error.rs` at tag 1.85.0 (`Read::read`, `read_exact`, `ErrorKind`) | implementation-doc | full text. Note: on master, `io` types are being moved to `alloc_crate::io`, so the stable tag was used |
| S6 | OpenJDK `java/io/InputStream.java`, `EOFException.java`, `DataInputStream.java` (master) | implementation-doc (Javadoc API spec) | full text |
| S7 | CPython `Doc/library/io.rst` (main) | implementation-doc | full text |
| S8 | CPython `Lib/gzip.py` (main) | implementation (code) | full text |
| S9 | dotnet-api-docs `xml/System.IO/Stream.xml` (main) | implementation-doc | full text |
| S10 | Node.js `doc/api/stream.md` (main) | implementation-doc | full text |
| S11 | WHATWG Streams Living Standard (Last Updated 25 October 2026), §4.4, §4.5 | normative (living standard) | full text |
| S12 | RFC 9112 HTTP/1.1 (2022), §6.3, §8, §9.8 | normative | full text |
| S13 | RFC 8446 TLS 1.3 (2018), §6.1 | normative | full text |
| L1 | Gunawi et al., "EIO: Error Handling is Occasionally Correct", FAST 2008 | peer-reviewed | lead only; NOT READ (file-system error propagation, probably another track's scope) |

No peer-reviewed empirical study of how callers mishandle short reads or EOF-versus-error in language stream APIs
was found in one search. That is a COVERAGE-GAP, not proof that none exists.

## Extracted findings

### C (S1, N1570)
- §7.21.2p3: "A binary stream is an ordered sequence of characters that can transparently record internal data. Data read in from a binary stream shall compare equal to the data that were earlier written out to that stream, under the same implementation. Such a stream may, however, have an implementation-defined number of null characters appended to the end of the stream."
  So the standard permits trailing NUL padding, and the byte length a reader observes need not equal the length written.
- §7.21.8.1p2-3 (fread): "If an error occurs, the resulting value of the file position indicator for the stream is indeterminate. If a partial element is read, its value is indeterminate." "returns the number of elements successfully read, which may be less than nmemb if a read error or end-of-file is encountered."
  The short count alone does not say whether EOF or an error happened.
- §7.21.7.1p3 (fgetc): "If the end-of-file indicator for the stream is set, or if the stream is at end-of-file, the end-of-file indicator for the stream is set and the fgetc function returns EOF ... If a read error occurs, the error indicator for the stream is set and the fgetc function returns EOF." Footnote 289: "An end-of-file and a read error can be distinguished by use of the feof and ferror functions."
  Both outcomes use the same in-band value (EOF), and the cause is kept in sticky per-stream indicators. Because the text says "If the end-of-file indicator ... is set", EOF is sticky: once the indicator is set, later reads return EOF even if data has since been appended.
- §7.21.10.2/3: feof/ferror return nonzero "if and only if" the respective indicator is set.

### POSIX read() (S2)
- "The value returned may be less than nbyte if the number of bytes left in the file is less than nbyte, if the read() request was interrupted by a signal, or if the file is a pipe or FIFO or special file and has fewer than nbyte bytes immediately available for reading."
- "If a read() is interrupted by a signal before it reads any data, it shall return -1 with errno set to [EINTR]. If a read() is interrupted by a signal after it has successfully read some data, it shall return the number of bytes read."
- "No data transfer shall occur past the current end-of-file. If the starting position is at or after the end-of-file, 0 shall be returned."
- Holes: "If any portion of a regular file prior to the end-of-file has not been written, read() shall return bytes with value 0."
- Empty pipe: "If no process has the pipe open for writing, read() shall return 0 to indicate end-of-file." With O_NONBLOCK and a writer present: -1 / EAGAIN.
- RATIONALE: "This volume of POSIX.1-2024 does not specify the value of the file offset after an error is returned; there are too many cases." "It is considered beyond the scope of this volume of POSIX.1-2024 to describe what happens in the case of hardware errors." On the history: AT&T systems returned -1/EINTR after a partial transfer, BSD and FIPS 151-x returned the count, and POSIX chose the count. Also: "an interrupt arriving earlier may not cause read() to return a partial byte count, but rather to return -1 and set errno to [EINTR]."
- Model: the result is a single value, either a count or -1 with errno. The rationale says outright that an error together with a short count was rejected ("contradictory to the idea that when errno is set, the function responsible shall return -1").

### Go (S3, S4)
- `io.Reader`: "Read reads up to len(p) bytes into p. It returns the number of bytes read (0 <= n <= len(p)) and any error encountered." "If some data is available but not len(p) bytes, Read conventionally returns what is available instead of waiting for more."
- "When Read encounters an error or end-of-file condition after successfully reading n > 0 bytes, it returns the number of bytes read. It may return the (non-nil) error from the same call or return the error (and n == 0) from a subsequent call. ... a Reader returning a non-zero number of bytes at the end of the input stream may return either err == EOF or err == nil. The next Read should return 0, EOF."
- "Callers should always process the n > 0 bytes returned before considering the error err."
- "Implementations of Read are discouraged from returning a zero byte count with a nil error ... Callers should treat a return of 0 and nil as indicating that nothing happened; in particular it does not indicate EOF."
- `io.EOF`: "Functions should return EOF only to signal a graceful end of input. If the EOF occurs unexpectedly in a structured data stream, the appropriate error is either [ErrUnexpectedEOF] or some other error giving more detail." "Read must return EOF itself, not an error wrapping EOF, because callers will test for EOF using ==."
- `ErrUnexpectedEOF`: "EOF was encountered in the middle of reading a fixed-size block or data structure."
- `ErrNoProgress`: "returned by some clients of a [Reader] when many calls to Read have failed to return any data or error, usually the sign of a broken [Reader] implementation."
- `ReadFull`: "The error is EOF only if no bytes were read. If an EOF happens after reading some but not all the bytes, ReadFull returns [ErrUnexpectedEOF]. On return, n == len(buf) if and only if err == nil. If r returns an error having read at least len(buf) bytes, the error is dropped."
- `encoding/binary.Read` follows the same rule (lines 255-257).
- `compress/gzip.Reader` (framed format with a trailer): "The Reader will return an [ErrChecksum] when [Reader.Read] reaches the end of the uncompressed data if it does not have the expected length or checksum. Clients should treat data returned by [Reader.Read] as tentative until they receive the [io.EOF] marking the end of the data." It also has a helper `noEOF` that "converts io.EOF to io.ErrUnexpectedEOF".
- Model: the result is a pair (n, err), and a single call may return both. EOF is a distinguished sentinel for a graceful end. A layer that knows the expected structure turns an EOF that arrives mid-structure into "unexpected EOF".

### Rust (S5, std 1.85.0)
- `Read::read`: "This function does not provide any guarantees about whether it blocks waiting for data, but if an object needs to block for a read and cannot, it will typically signal this via an [`Err`] return value."
- "If `n` is `0`, then it can indicate one of two scenarios: 1. This reader has reached its "end of file" and will likely no longer be able to produce bytes. Note that this does not mean that the reader will *always* no longer be able to produce bytes ... for [`File`], it is possible to reach the end of file and get zero as result, but if more data is appended to the file, future calls to `read` will return more data. 2. The buffer specified was 0 bytes in length."
  So EOF is not sticky by contract. Compare C fgetc above.
- "It is not an error if the returned value `n` is smaller than the buffer size, even when the reader is not at the end of the stream yet."
- "If an error is returned then it must be guaranteed that no bytes were read." This is stricter than Go, which allows n>0 together with an error.
- "An error of the [`ErrorKind::Interrupted`] kind is non-fatal and the read operation should be retried if there is nothing else to do."
- Safety note: "As this trait is safe to implement, callers in unsafe code cannot rely on `n <= buf.len()` for safety."
- `read_exact`: "If this function encounters an "end of file" before completely filling the buffer, it returns an error of the kind [`ErrorKind::UnexpectedEof`]. The contents of `buf` are unspecified in this case." "If this function returns an error, it is unspecified how many bytes it has read, but it will never read more than would be necessary to completely fill the buffer."
- `ErrorKind::UnexpectedEof` (error.rs): "An error returned when an operation could not be completed because an "end of file" was reached prematurely. This typically means that an operation could only succeed if it read a particular number of bytes but only a smaller number of bytes could be read." `WouldBlock`: "The operation needs to block to complete, but the blocking operation was requested to not occur." `Interrupted`: "Interrupted operations can typically be retried."

### Java (S6)
- `read(byte[],int,int)`: "An attempt is made to read as many as len bytes, but a smaller number may be read." "This method blocks until input data is available, end of file is detected, or an exception is thrown." "If no byte is available because the stream is at end of file, the value -1 is returned; otherwise, at least one byte is read."
- @implSpec of the default `InputStream.read(b,off,len)`: "If any subsequent call to read() results in a IOException, the exception is caught and treated as if it were end of file; the bytes read up to that point are stored into b and the number of bytes read before the exception occurred is returned."
  So the base-class default turns an I/O error that comes after the first byte into a short read. The error is not lost permanently, only deferred, because the next call usually fails on its first byte. (Inference: a caller that stops on a short count or a -1 may never see the error.)
- `readNBytes(int)`: "Fewer than len bytes may be read if end of stream is encountered." Also: "The behavior for the case where the input stream is asynchronously closed, or the thread interrupted during the read, is highly input stream specific, and therefore not specified."
- `readNBytes(byte[],int,int)`: "In the case where end of stream is reached before len bytes have been read, then the actual number of bytes read will be returned." This method does not raise an exception on truncation.
- `available()`: "Returns an estimate ... It is never correct to use the return value of this method to allocate a buffer intended to hold all data in this stream."
- `EOFException`: "Signals that an end of file or end of stream has been reached unexpectedly during input. ... Note that many other input operations return a special value on end of stream rather than throwing an exception." `DataInputStream.readFully` throws EOFException when `count < 0`. `skipNBytes` throws EOFException.

### Python (S7, S8)
- `RawIOBase.read`: "Attempts to make only one system call but will retry if interrupted and the signal handler does not raise an exception (see PEP 475 ...). This means fewer than size bytes may be returned if the operating system call returns fewer than size bytes. If 0 bytes are returned, and size was not 0, this indicates end of file. If the object is in non-blocking mode and no bytes are available, None is returned."
- `RawIOBase.readinto`: the same distinction (0 means EOF, None means no data available in non-blocking mode).
- `BufferedIOBase.read`: "Fewer bytes may be returned than requested. An empty bytes object is returned if the stream is already at EOF. ... Less than size bytes being returned does not imply that EOF is imminent." Note: "When the underlying raw stream is non-blocking, implementations may either raise BlockingIOError or return None if no data is available. io implementations return None."
- `BufferedIOBase.readinto`: "A BlockingIOError is raised if the underlying raw stream is in non blocking-mode, and has no data available at the moment."
- `BufferedReader.peek`: "If the underlying raw stream is non-blocking and the operation would block, returns empty bytes." Empty bytes is also the EOF signal for `read`, so peek uses one value for two conditions.
- Python's gzip module (framed format) raises `EOFError("Compressed file ended before the end-of-stream marker was reached")` when the underlying read returns b"" before the deflate end marker or before the 8-byte trailer. This turns a raw EOF into a truncation error.

### .NET (S9)
- `Stream.Read`: "If more than zero bytes are requested, the implementation will not complete the operation until at least one byte of data can be read ... Read returns 0 only if zero bytes were requested or when there is no more data in the stream and no more is expected (such as a closed socket or end of file). An implementation is free to return fewer bytes than requested even if the end of the stream has not been reached."
- "The current position within the stream is advanced by the number of bytes read; however, if an exception occurs, the current position within the stream remains unchanged." This is a stronger postcondition than C (indeterminate), POSIX (unspecified) and Rust read_exact (unspecified count).
- `ReadAtLeast(buffer, minimumBytes, throwOnEndOfStream=true)`: the return is "guaranteed to be greater than or equal to minimumBytes when throwOnEndOfStream is true", and it throws `EndOfStreamException` otherwise. `ReadExactly`: `EndOfStreamException` "The end of the stream is reached before filling the buffer."

### Node.js (S10)
- `'end'`: "emitted when there is no more data to be consumed from the stream. The 'end' event will not be emitted unless the data is completely consumed."
- `'error'`: "may be emitted by a Readable implementation at any time."
- `readable.read(size)`: "If no data is available to be read, null is returned. ... If size bytes are not available to be read, null will be returned unless the stream has ended, in which case all of the data remaining in the internal buffer will be returned."
- `stream.finished`: "notified when a stream is no longer readable, writable or has experienced an error or a premature close event ... a stream is destroyed prematurely (like an aborted HTTP request), and will not emit 'end' or 'finish'." Changelog v14.0.0: "Emitting 'close' before 'end' on a Readable stream will cause an ERR_STREAM_PREMATURE_CLOSE error."
- Model: an event-based state machine with separate channels for data, end, error and close. A "premature close" (close without end) is classified explicitly.

### WHATWG Streams (S11)
- `ReadableStreamDefaultReader.read()`: fulfilled with `{ value: theChunk, done: false }`; "If the stream becomes closed, the promise will be fulfilled with an object of the form { value: undefined, done: true }. If the stream becomes errored, the promise will be rejected with the relevant error."
- The stream state is one "of "readable", "closed", or "errored"".
- BYOB `read(view, {min})`: "If the stream becomes closed, then the promise is fulfilled with the remaining elements in the stream, which might be fewer than the initially requested amount. If not given, then the promise resolves when at least one element is available." Cancellation also yields `{ value: undefined, done: true }`, so the reader sees canceled and closed the same way.

### Framing and truncation detectability (S12, S13)
- RFC 9112 §6.3: "Since there is no way to distinguish a successfully completed, close-delimited response message from a partially received message interrupted by network failure, a server SHOULD generate encoding or length-delimited messages whenever possible."
- §8: "A message body that uses the chunked transfer coding is incomplete if the zero-sized chunk that terminates the encoding has not been received. A message that uses a valid Content-Length is incomplete if the size of the message body received (in octets) is less than the value given by Content-Length." "A client that receives an incomplete response message ... MUST record the message as incomplete."
- §9.8: "A response that has neither chunked transfer coding nor Content-Length is complete only if a valid closure alert has been received. Treating an incomplete message as complete could expose implementations to attack."
- RFC 8446 §6.1: "The client and the server must share knowledge that the connection is ending in order to avoid a truncation attack." "If a transport-level close is received prior to a "close_notify", the receiver cannot know that all the data that was sent has been received."

## Existing models and classifications found (source terminology kept)
1. **In-band sentinel plus sticky indicators** (C stdio): EOF is returned for both end-of-file and read error. The cause is told apart through the end-of-file indicator and the error indicator (feof/ferror).
2. **Count-or-error single return** (POSIX read): either a count >= 0 or -1 with errno. Short counts have three enumerated causes. 0 means end-of-file. EINTR means interrupted before any data. EAGAIN means non-blocking with no data.
3. **(n, err) pair with deferred error** (Go io.Reader): data and an error may arrive together. A graceful end is shown by the `EOF` sentinel. Truncation inside a structure is `ErrUnexpectedEOF`.
4. **Ok(n) / Err exclusive** (Rust Read): Ok(0) means EOF or an empty buffer. An Err guarantees no bytes were read. ErrorKind has `Interrupted` (retry), `WouldBlock` and `UnexpectedEof`.
5. **-1 / IOException** (Java): -1 means end of stream. An exception is an error. `EOFException` means an unexpected end, used by the DataInput and readFully family.
6. **Three-valued raw read** (Python io): b'' or 0 means EOF, None means no data available in non-blocking mode, and bytes means data. Buffered layers may raise BlockingIOError instead of returning None.
7. **0-or-exception plus exact-read helpers** (.NET): 0 means end of stream. `EndOfStreamException` comes from ReadExactly or ReadAtLeast.
8. **Event and state machine** (Node streams; WHATWG streams): readable, closed and errored states. `'end'`, `'error'` and `'close'` are separate events. Premature close is a named error.
9. **"Exact-read" combinator pattern**, convergent across languages: Go ReadFull, Rust read_exact, Java readFully/readNBytes, .NET ReadExactly/ReadAtLeast. These helpers turn "short read at EOF" into an "unexpected EOF" class. Java `readNBytes(byte[],..)` is the exception and returns a short count.
10. **Framed versus close-delimited message** (RFC 9112): truncation is detectable only when length or a terminator is encoded in-band. RFC 8446 adds that an authenticated closure (close_notify) is needed to tell an orderly close from truncation at the transport layer.

## Convergences
- Every contract read here lets a single read return fewer bytes than requested when no end-of-stream has occurred: C (fread "may be less"), POSIX, Go, Rust, Java, Python, .NET, and WHATWG BYOB with min. In none of them is a short read by itself a signal of EOF or of error.
- Graceful end versus truncation is not decided by the byte-stream layer. It is introduced by a caller or a layer that knows an expected length: Go's EOF doc, Rust UnexpectedEof, Java EOFException, gzip readers, RFC 9112 §8.
- Most low-level APIs report "no data available right now" in non-blocking mode separately from EOF: POSIX EAGAIN, Rust WouldBlock, Python None / BlockingIOError, Node null.

## Contradictions and divergences
- **Data together with an error in one call.** Go allows n>0 with err!=nil. Rust requires "no bytes were read" when Err is returned. POSIX deliberately rejected "setting errno to [EINTR] while returning a short count".
- **Sticky EOF.** C fgetc returns EOF whenever the end-of-file indicator is set. Rust says Ok(0) "does not mean that the reader will *always* no longer be able to produce bytes". Go says the next Read "should" return 0, EOF.
- **Position after error.** C: indeterminate. POSIX: unspecified ("too many cases"). Rust read_exact: unspecified count. .NET Stream.Read: "remains unchanged".
- **An error converted into a short read or EOF.** Java's default `InputStream.read(b,off,len)` catches a later IOException and treats it "as if it were end of file". Go ReadFull drops an error that arrives after len(buf) bytes. Both conflict with the advice elsewhere to process the error.
- **Python non-blocking signalling is inconsistent across layers.** RawIOBase.read returns None. BufferedIOBase.read may raise BlockingIOError or return None, and io returns None. BufferedIOBase.readinto raises BlockingIOError. BufferedReader.peek returns empty bytes, which is the EOF value elsewhere.
- **0 / nil in Go** is "nothing happened" and not EOF. In POSIX, Rust, Python, .NET and Java's readNBytes, a zero return means EOF (for a non-empty buffer).
- **WHATWG cancel vs close**: BYOB read after cancel fulfills `{ value: undefined, done: true }`, which looks like a close to the reader.

## Gaps
- GENUINE-GAP (as far as this track saw): none of the language contracts gives a way to tell, at the byte-stream layer, a completed unframed stream from a truncated one. RFC 9112 §6.3 says so outright for close-delimited messages. Detection is left to framing (lengths, terminators, checksums) or to authenticated closure.
- GENUINE-GAP: hardware or media errors during a read are out of scope for POSIX ("beyond the scope"). The language docs do not say whether an I/O error is transient or permanent, except that Interrupted/EINTR can be retried.
- COVERAGE-GAP: no peer-reviewed empirical study of misuse of short-read or EOF contracts was read. One lead (Gunawi et al. FAST 2008 EIO) was not read.
- COVERAGE-GAP: no formal semantics of streams was read (e.g., Kahn process networks, coinductive stream semantics, session types for I/O protocols).
- COVERAGE-GAP: the published ISO C text was not read (paywall). N1570 is the committee draft, and the C17/C23 wording was not checked.
- COVERAGE-GAP: Rust master now re-exports io types from `alloc_crate::io`. The 1.85.0 wording was used and not checked against the newest doc text.
