#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define	pdir	CBOR
%define	pnam	XS
Summary:	CBOR::XS - Concise Binary Object Representation (CBOR, RFC7049)
Summary(pl.UTF-8):	CBOR::XS - Concise Binary Object Representation (CBOR, RFC7049)
Name:		perl-CBOR-XS
Version:	1.7
Release:	1
Epoch:		2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/M/ML/MLEHMANN/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	dfe163f8b9d9a890a445bced9cba1cca
URL:		http://search.cpan.org/dist/CBOR-XS/
BuildRequires:	perl-Canary-Stability
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Encode
BuildRequires:	perl-Types-Serialiser
BuildRequires:	perl-common-sense
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module converts Perl data structures to the Concise Binary Object
Representation (CBOR) and vice versa. CBOR is a fast binary
serialisation format that aims to use an (almost) superset of the JSON
data model, i.e. when you can represent something useful in JSON, you
should be able to represent it in CBOR.

In short, CBOR is a faster and quite compact binary alternative to
JSON, with the added ability of supporting serialisation of Perl
objects. (JSON often compresses better than CBOR though, so if you
plan to compress the data later and speed is less important you might
want to compare both formats first).

%description -l pl.UTF-8
Ten moduł konwertuje struktury danych Perla do formatu CBOR (Concise
Binary Object Representation) i odwrotnie. CBOR jest szybkim binarnym
formatem serializacji, którego celem jest używanie nadzbioru
możliwości JSONa, tzn. gdy coś da się reprezentować w
formacie JSON, da się również to zrobić w formacie CBOR.

W skrócie, CBOR jest szybszą i bardziej kompaktową alternatywą
dla formatu JSON, z możliwością wspierania serializacji obiektów
Perla. Jednakże, często JSON lepiej się kompresuje niż CBOR,
więc jeżeli planujesz kompresować później dane, a prędkość
nie jest istotna, możesz chcieć najpierw porównać oba formaty.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
export PERL_CANARY_STABILITY_NOPROMPT=1
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorarch}/CBOR
%{perl_vendorarch}/CBOR/XS.pm
%dir %{perl_vendorarch}/auto/CBOR
%dir %{perl_vendorarch}/auto/CBOR/XS
%attr(755,root,root) %{perl_vendorarch}/auto/CBOR/XS/*.so
%{_mandir}/man3/CBOR::XS.3pm*
%{_examplesdir}/%{name}-%{version}
