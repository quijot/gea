# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from gea.models import Expediente
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response, RequestContext

from django import forms
from django.shortcuts import render

ftp_url = 'ftp://zentyal.estudio.lan'

def index(request):
    template = loader.get_template('portada.html')
    context  = Context({
    })
    return HttpResponse(template.render(context))

def listado_comun(request):
    exp_list   = Expediente.objects.order_by('-id')
    paginator = Paginator(exp_list, 20)
    page = request.GET.get('page')
    try:
        expedientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        expedientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        expedientes = paginator.page(paginator.num_pages)
    template = loader.get_template('listado_comun.html')
    context  = Context({
        'cl': expedientes,
    })
    return HttpResponse(template.render(context))

#
# Solicitud de inscripcion SCIT
#
CP = (
  (u'S2124XAD', u"22 DE MAYO"),
  (u'S2732XAA', u"4 DE FEBRERO"),
  (u'S6106', u"AARÓN CASTELLANOS"),
  (u'S3042XAA', u"ABIPONES"),
  (u'S2109', u"ACEBAL"),
  (u'S2344XAA', u"ACHAVAL RODRIGUEZ"),
  (u'S2311XAC', u"ADOLFO ALSINA"),
  (u'S2132XAC', u"AERO CLUB ROSARIO"),
  (u'S3071XAA', u"AGUARÁ GRANDE"),
  (u'S2101', u"ALBARELLOS"),
  (u'S2117', u"ALCORTA"),
  (u'S2214', u"ALDAO"),
  (u'S3051', u"ALEJANDRA"),
  (u'S3550XAE', u"ALLENDE"),
  (u'S3001XAM', u"ALTO VERDE"),
  (u'S2107', u"ÁLVAREZ"),
  (u'S2126', u"ALVEAR"),
  (u'S2352', u"AMBROSETTI"),
  (u'S6103', u"AMENÁBAR"),
  (u'S2214', u"ANDINO"),
  (u'S3014', u"ANGEL GALLARDO"),
  (u'S2303', u"ANGÉLICA"),
  (u'S3048', u"ANGELONI"),
  (u'S3061XAI', u"ANTONIO PINI"),
  (u'S2183XAB', u"AREQUITO"),
  (u'S2242XAA', u"ARIJON"),
  (u'S2119', u"ARMINDA"),
  (u'S2508', u"ARMSTRONG"),
  (u'S2242', u"AROCENA"),
  (u'S3036XAB', u"AROMOS"),
  (u'S3046XAK', u"ARRASCAETA"),
  (u'S3014', u"ARROYO AGUIAR"),
  (u'S3575', u"ARROYO CEIBAL"),
  (u'S3565XAA', u"ARROYO DEL REY"),
  (u'S3001XAP', u"ARROYO LEYES"),
  (u'S2128', u"ARROYO SECO"),
  (u'S2344', u"ARRUFÓ"),
  (u'S2156XAB', u"ARSENAL DE GUERRA SAN LORENZO"),
  (u'S2187', u"ARTEAGA"),
  (u'S3014XAG', u"ASCOCHINGAS"),
  (u'S3040XAG', u"ASUNCION MARIA"),
  (u'S2307', u"ATALIVA"),
  (u'S2318', u"AURELIA"),
  (u'S2318XAA', u"AURELIA NORTE"),
  (u'S2318XAB', u"AURELIA SUD"),
  (u'S3561', u"AVELLANEDA"),
  (u'S2449XAA', u"AVENA"),
  (u'S3040XAC', u"AVICHUNCHO"),
  (u'S3017XAA', u"BAJO LAS TUNAS"),
  (u'S2175XAA', u"BARLETT"),
  (u'S2246', u"BARRANCAS"),
  (u'S3000XAD', u"BARRANQUITAS"),
  (u'S2440XAA', u"BARRIO BELGRANO ORTIZ"),
  (u'S2242', u"BARRIO CAIMA"),
  (u'S3569', u"BARROS PAZOS"),
  (u'S2403XAA', u"BAUER Y SIGEL"),
  (u'S2326XAE', u"BEALISTOCK"),
  (u'S2301', u"BELLA ITALIA"),
  (u'S2639', u"BERABEVÚ"),
  (u'S3569', u"BERNA"),
  (u'S2119XAA', u"BERNARD"),
  (u'S2248', u"BERNARDO DE IRIGOYEN"),
  (u'S2501XAC', u"BERRETTA"),
  (u'S2177', u"BIGAND"),
  (u'S2600XAB', u"BOCA P 25"),
  (u'S2179', u"BOMBAL"),
  (u'S2156XAC', u"BORGHI"),
  (u'S2326', u"BOSSI"),
  (u'S2523', u"BOUQUET"),
  (u'S2501', u"BUSTINZA"),
  (u'S3036', u"CABAL"),
  (u'S2322', u"CABAÑA EL CISNE"),
  (u'S3061XAC', u"CABEZA DE CHANCHO"),
  (u'S3041XAB', u"CACIQUE ARIACAIQUÍN"),
  (u'S2643', u"CAFFERATA"),
  (u'S3050', u"CALCHAQUÍ"),
  (u'S3001XAA', u"CALCHINES"),
  (u'S2720XAA', u"CAMINERA GENERAL LÓPEZ"),
  (u'S2126XAA', u"CAMINO MONTE FLORES"),
  (u'S3021', u"CAMPO ANDINO"),
  (u'S3046XAL', u"CAMPO BERRAZ"),
  (u'S2345XAA', u"CAMPO BOTTO"),
  (u'S2248XAB', u"CAMPO BRARDA"),
  (u'S2123XAA', u"CAMPO CALVO"),
  (u'S2248XAC', u"CAMPO CARIGNANO"),
  (u'S2148XAB', u"CAMPO CASTRO"),
  (u'S2512XAC', u"CAMPO CHARO"),
  (u'S2407XAA', u"CAMPO CLUCELLAS"),
  (u'S3056XAA', u"CAMPO COUBERT"),
  (u'S2185XAA', u"CAMPO CRENNA"),
  (u'S3001XAQ', u"CAMPO CRESPO"),
  (u'S2307XAA', u"CAMPO DARATTI"),
  (u'S3001XAB', u"CAMPO DEL MEDIO"),
  (u'S3569XAA', u"CAMPO EL ARAZA"),
  (u'S2342XAA', u"CAMPO EL MATACO"),
  (u'S2440XAB', u"CAMPO FAGGIANO"),
  (u'S3569XAB', u"CAMPO FURRER"),
  (u'S2212XAA', u"CAMPO GALLOSO"),
  (u'S3572XAA', u"CAMPO GARABATO"),
  (u'S3066XAB', u"CAMPO GARAY"),
  (u'S2240XAC', u"CAMPO GARCIA"),
  (u'S2248XAD', u"CAMPO GENERO"),
  (u'S2508XAB', u"CAMPO GIMBATTI"),
  (u'S2253XAA', u"CAMPO GIMENEZ"),
  (u'S3516XAA', u"CAMPO GOLA"),
  (u'S3575XAF', u"CAMPO GRANDE"),
  (u'S2144XAB', u"CAMPO HORQUESCO"),
  (u'S3555XAB', u"CAMPO HUBER"),
  (u'S3001XAC', u"CAMPO ITURRASPE"),
  (u'S2508XAA', u"CAMPO LA AMISTAD"),
  (u'S2512XAB', u"CAMPO LA PAZ"),
  (u'S2505XAA', u"CAMPO LA RIVIERE"),
  (u'S3014XAA', u"CAMPO LEHMAN"),
  (u'S3011XAC', u"CAMPO MAGNIN"),
  (u'S2142XAA', u"CAMPO MEDINA"),
  (u'S3551XAK', u"CAMPO MONTE LA VIRUELA"),
  (u'S2240XAD', u"CAMPO MOURE"),
  (u'S2639XAA', u"CAMPO NUEVO"),
  (u'S2206XAA', u"CAMPO PALETTA"),
  (u'S2173XAA', u"CAMPO PESOA"),
  (u'S2258', u"CAMPO QUIÑONES"),
  (u'S2607XAA', u"CAMPO QUIRNO"),
  (u'S2216XAA', u"CAMPO RAFFO"),
  (u'S3572XAE', u"CAMPO RAMSEYER"),
  (u'S3581XAF', u"CAMPO REDONDO"),
  (u'S2255XAA', u"CAMPO RODRIGUEZ"),
  (u'S2407XAB', u"CAMPO ROMERO"),
  (u'S2109XAA', u"CAMPO RUEDA"),
  (u'S3060XAF', u"CAMPO SAN JOSÉ"),
  (u'S2505XAB', u"CAMPO SANTA ISABEL"),
  (u'S3020XAA', u"CAMPO SANTO DOMINGO"),
  (u'S3575XAG', u"CAMPO SIETE PROVINCIAS"),
  (u'S2403XAB', u"CAMPO TORQUINSTON"),
  (u'S3560XAF', u"CAMPO UBAJO"),
  (u'S3516XAC', u"CAMPO VERGE"),
  (u'S3586XAC', u"CAMPO YAGUARETE"),
  (u'S3045XAA', u"CAMPO ZAVALLA"),
  (u'S2407XAC', u"CAMPO ZURBRIGGEN"),
  (u'S2170XAA', u"CANDELARIA SUD"),
  (u'S3018', u"CANDIOTI"),
  (u'S2500', u"CAÑADA DE GOMEZ"),
  (u'S2635', u"CAÑADA DEL UCLE"),
  (u'S3551', u"CAÑADA OMBU"),
  (u'S2105', u"CAÑADA RICA"),
  (u'S2454', u"CAÑADA ROSQUIN"),
  (u'S3052', u"CAÑADITA"),
  (u'S3574XAA', u"CAPILLA GUADALUPE NORTE"),
  (u'S2301XAA', u"CAPILLA SAN JOSÉ"),
  (u'S2154', u"CAPITÁN BERMÚDEZ"),
  (u'S2311XAF', u"CAPIVARA"),
  (u'S3557XAA', u"CARAGUATAY"),
  (u'S2138', u"CARCARAÑA"),
  (u'S2240XAA', u"CARCEL MODELO CORONDA"),
  (u'S2635XAA', u"CARLOS DOSE"),
  (u'S2453', u"CARLOS PELLEGRINI"),
  (u'S2618', u"CARMEN"),
  (u'S2109', u"CARMEN DEL SAUCE"),
  (u'S2729', u"CARRERAS"),
  (u'S2218XAA', u"CARRIZALES"),
  (u'S2317', u"CASABLANCA"),
  (u'S2248XAA', u"CASALEGNO"),
  (u'S2148', u"CASAS"),
  (u'S2170', u"CASILDA"),
  (u'S2401', u"CASTELAR"),
  (u'S3081', u"CAVOUR"),
  (u'S3001', u"CAYASTÁ"),
  (u'S3038', u"CAYASTACITO"),
  (u'S2148', u"CENTENO"),
  (u'S2105', u"CEPEDA"),
  (u'S2202XAA', u"CERANA"),
  (u'S2340', u"CERES"),
  (u'S3550XAD', u"CERRITO"),
  (u'S2173', u"CHABÁS"),
  (u'S2643', u"CHAÑAR LADEADO"),
  (u'S2603', u"CHAPUY"),
  (u'S2600XAC', u"CHATEAUBRIAND"),
  (u'S2633', u"CHOVET"),
  (u'S2500XAA', u"CICARELLI"),
  (u'S2218', u"CLARKE"),
  (u'S2146', u"CLASON"),
  (u'S2407', u"CLUCELLAS"),
  (u'S3001XAN', u"COLASTINÉ"),
  (u'S3001XAO', u"COLASTINÉ NORTE"),
  (u'S3551XAM', u"COLMENA"),
  (u'S3029XAA', u"COLONIA ADOLFO ALSINA"),
  (u'S2317XAB', u"COLONIA ALDAO"),
  (u'S3572XAB', u"COLONIA ALTHUAUS"),
  (u'S2345XAB', u"COLONIA ANA"),
  (u'S2257', u"COLONIA BELGRANO"),
  (u'S2300XAD', u"COLONIA BELLA ITALIA"),
  (u'S2313XAG', u"COLONIA BERLIN"),
  (u'S2317XAC', u"COLONIA BICHA"),
  (u'S2317XAD', u"COLONIA BIGAND"),
  (u'S3005XAA', u"COLONIA CALIFORNIA"),
  (u'S3036XAA', u"COLONIA CAMPO BOTTO"),
  (u'S2170XAB', u"COLONIA CANDELARIA"),
  (u'S2301', u"COLONIA CASTELLANOS"),
  (u'S2405XAA', u"COLONIA CELLO"),
  (u'S3025XAD', u"COLONIA CLARA"),
  (u'S2123XAB', u"COLONIA CLODOMIRA"),
  (u'S2240XAB', u"COLONIA CORONDINA"),
  (u'S3045XAE', u"COLONIA DOLORES"),
  (u'S2349', u"COLONIA DOS ROSAS Y LA LEGUA"),
  (u'S3553XAB', u"COLONIA DURAN"),
  (u'S2138XAA', u"COLONIA EL CARMEN"),
  (u'S3042XAB', u"COLONIA EL OCHENTA"),
  (u'S3074XAC', u"COLONIA EL SIMBOL"),
  (u'S3553XAC', u"COLONIA EL TOBA"),
  (u'S3560XAB', u"COLONIA EL VEINTICINCO"),
  (u'S3572XAC', u"COLONIA ELLA"),
  (u'S2103XAB', u"COLONIA ESCRIBANO"),
  (u'S2639XAB', u"COLONIA FERNANDEZ"),
  (u'S3005XAB', u"COLONIA FRANCESA"),
  (u'S2639XAC', u"COLONIA GOMEZ"),
  (u'S2637XAA', u"COLONIA HANSEN"),
  (u'S3592', u"COLONIA HARDY"),
  (u'S3066XAC', u"COLONIA INDEPENDENCIA"),
  (u'S2403', u"COLONIA JOSEFINA"),
  (u'S3052XAB', u"COLONIA LA BLANCA"),
  (u'S2637', u"COLONIA LA CATALANA"),
  (u'S2170XAC', u"COLONIA LA COSTA"),
  (u'S3056XAC', u"COLONIA LA MARIA"),
  (u'S3045XAB', u"COLONIA LA MORA"),
  (u'S3054XAF', u"COLONIA LA NEGRA"),
  (u'S3056XAB', u"COLONIA LA NICOLASA"),
  (u'S3081XAA', u"COLONIA LA NUEVA"),
  (u'S2639', u"COLONIA LA PALENCIA"),
  (u'S2639', u"COLONIA LA PELLEGRINI"),
  (u'S3045XAF', u"COLONIA LA PENCA"),
  (u'S2451XAB', u"COLONIA LA YERBA"),
  (u'S2187XAA', u"COLONIA LAGO DI COMO"),
  (u'S3003XAA', u"COLONIA LOS ZAPALLOS"),
  (u'S2347XAA', u"COLONIA MACKINLAY"),
  (u'S2347XAB', u"COLONIA MALHMAN SUD"),
  (u'S3046XAM', u"COLONIA MANUEL MENCHACA"),
  (u'S2443XAA', u"COLONIA MARGARITA"),
  (u'S3001XAW', u"COLONIA MASCÍAS"),
  (u'S3013XAA', u"COLONIA MATILDE"),
  (u'S2311XAA', u"COLONIA MAUÁ"),
  (u'S2144XAA', u"COLONIA MÉDICI"),
  (u'S2341XAA', u"COLONIA MONTEFIORE"),
  (u'S2609XAA', u"COLONIA MORGAN"),
  (u'S3001XAD', u"COLONIA NUEVA NARCISO"),
  (u'S2313XAB', u"COLONIA ORTIZ"),
  (u'S2252XAA', u"COLONIA PIAGGIO"),
  (u'S2639XAH', u"COLONIA PIAMONTESA"),
  (u'S3080XAB', u"COLONIA PUJOL"),
  (u'S2309XAA', u"COLONIA REINA MARGARITA"),
  (u'S2349XAA', u"COLONIA RIPAMONTI"),
  (u'S2347', u"COLONIA ROSA"),
  (u'S3553XAD', u"COLONIA SAGER"),
  (u'S2301', u"COLONIA SAN ANTONIO"),
  (u'S2527XAA', u"COLONIA SAN FRANCISCO"),
  (u'S3001XAE', u"COLONIA SAN JOAQUÍN"),
  (u'S3563XAA', u"COLONIA SAN MANUEL"),
  (u'S3005XAI', u"COLONIA SAN ROQUE"),
  (u'S2451XAA', u"COLONIA SANTA ANITA"),
  (u'S3572XAD', u"COLONIA SANTA CATALINA"),
  (u'S2609XAB', u"COLONIA SANTA LUCÍA"),
  (u'S2639XAI', u"COLONIA SANTA NATALIA"),
  (u'S3042XAC', u"COLONIA SILVA"),
  (u'S2324XAA', u"COLONIA TACURALES"),
  (u'S3005XAC', u"COLONIA TERESA"),
  (u'S2185XAC', u"COLONIA TOSCANA PRIMERA"),
  (u'S2185XAB', u"COLONIA TOSCANA SEGUNDA"),
  (u'S2216XAB', u"COLONIA TRES MARIAS"),
  (u'S3048XAA', u"COLONIA TRES REYES"),
  (u'S3516', u"COLONIA URDÁNIZ"),
  (u'S2115XAD', u"COLONIA VALDEZ"),
  (u'S2639XAD', u"COLONIA VALENCIA"),
  (u'S3560XAC', u"COLONIA YAGUARETE"),
  (u'S2311XAB', u"CONSTANZA"),
  (u'S3014XAB', u"CONSTITUYENTES"),
  (u'S2919XAB', u"COPACABANA"),
  (u'S2631XAA', u"CORA"),
  (u'S2240', u"CORONDA"),
  (u'S2124XAB', u"CORONEL AGUIRRE"),
  (u'S2123', u"CORONEL ARNOLD"),
  (u'S2103', u"CORONEL BOGADO"),
  (u'S2105', u"CORONEL DOMINGUEZ"),
  (u'S2301XAB', u"CORONEL FRAGA"),
  (u'S3013XAB', u"CORONEL RODRÍGUEZ"),
  (u'S6106XAA', u"CORONEL ROSETI"),
  (u'S2506', u"CORREA"),
  (u'S3553', u"COSTA DEL TOBA"),
  (u'S2126XAB', u"CRESTA"),
  (u'S2441', u"CRISPI"),
  (u'S2445XAA', u"CRISTOLIA"),
  (u'S2313XAC', u"CUATRO CASAS"),
  (u'S2639XAE', u"CUATRO ESQUINAS"),
  (u'S2202XAB', u"CULLEN"),
  (u'S3023XAE', u"CULULÚ"),
  (u'S2342', u"CURUPAYTI"),
  (u'S3567XAB', u"DEST AERONAUTICO MILIT RECONQU"),
  (u'S2242', u"DESVÍO ARIJÓN"),
  (u'S2415XAA', u"DESVÍO BOERO"),
  (u'S3551XAN', u"DESVÍO KILÓMETRO 282"),
  (u'S3551XAA', u"DESVÍO KILÓMETRO 392"),
  (u'S3070XAC', u"DHO"),
  (u'S2222', u"DÍAZ"),
  (u'S6036', u"DIEGO DE ALVEAR"),
  (u'S3575XAA', u"DISTRITO 3 ISLETAS"),
  (u'S2313XAD', u"DOCE CASAS"),
  (u'S2631XAB', u"DÚRHAM"),
  (u'S2301', u"EGUSQUIZA"),
  (u'S3550XAG', u"EL 38"),
  (u'S3550XAH', u"EL 44"),
  (u'S3070XAA', u"EL AGUARÁ"),
  (u'S6106XAF', u"EL ALBERDON"),
  (u'S3060XAG', u"EL AMARGO"),
  (u'S3563XAB', u"EL ARAZÁ"),
  (u'S2723XAA', u"EL BAGUAL"),
  (u'S2300XAB', u"EL BAYO"),
  (u'S3550XAA', u"EL BONETE"),
  (u'S2643XAA', u"EL CANTOR"),
  (u'S2105XAE', u"EL CARAMELO"),
  (u'S3561XAA', u"EL CARMEN DE AVELLANEDA"),
  (u'S3575XAH', u"EL CEIBALITO"),
  (u'S3005XAE', u"EL CEIBO"),
  (u'S3550XAF', u"EL CINCUENTA"),
  (u'S3553XAG', u"EL DIECISIETE"),
  (u'S3021XAA', u"EL GALPON"),
  (u'S3005XAF', u"EL GUSANO"),
  (u'S2732XAB', u"EL JARDÍN"),
  (u'S3001XAH', u"EL LAUREL"),
  (u'S3060XAH', u"EL MARIANO"),
  (u'S3061XAD', u"EL NOCHERO"),
  (u'S3051XAA', u"EL PAJARO BLANCO"),
  (u'S3005XAG', u"EL PARA"),
  (u'S3001XAI', u"EL POZO"),
  (u'S3592XAB', u"EL RABÓN"),
  (u'S6103XAC', u"EL REFUGIO"),
  (u'S3572XAF', u"EL RICARDITO"),
  (u'S3046XAQ', u"EL SOMBRERERO"),
  (u'S3585XAE', u"EL SOMBRERITO"),
  (u'S3565XAH', u"EL TAJAMAR"),
  (u'S3575XAI', u"EL TAPIALITO"),
  (u'S3561XAC', u"EL TIMBÓ"),
  (u'S2202XAC', u"EL TRANSITO"),
  (u'S2535', u"EL TRÉBOL"),
  (u'S3060XAN', u"EL TRIÁNGULO"),
  (u'S3009XAA', u"EL TROPEZÓN"),
  (u'S3029', u"ELISA"),
  (u'S2732', u"ELORTONDO"),
  (u'S3036', u"EMILIA"),
  (u'S3007XAB', u"EMPALME SAN CARLOS"),
  (u'S2918', u"EMPALME VILLA CONSTITUCIÓN"),
  (u'S2607XAB', u"ENCADENADAS"),
  (u'S2456', u"ESMERALDA"),
  (u'S2401XAA', u"ESMERALDITA"),
  (u'S3080', u"ESPERANZA"),
  (u'S3056XAE', u"ESPÍN"),
  (u'S3040XAB', u"ESQUINA GRANDE"),
  (u'S2611', u"ESTACION CHRISTOPHERSEN"),
  (u'S2407', u"ESTACIÓN CLUCELLAS"),
  (u'S2119XAB', u"ESTACIÓN ERASTO"),
  (u'S2403XAD', u"ESTACION JOSÉFINA"),
  (u'S2445XAC', u"ESTACIÓN MARÍA JUANA"),
  (u'S3013XAD', u"ESTACIÓN MATILDE"),
  (u'S2315XAA', u"ESTACION SAGUIER"),
  (u'S2600XAD', u"ESTACIÓN TEODELINA"),
  (u'S2919XAA', u"ESTACION VILLA CONSTITUCION"),
  (u'S3060XAE', u"ESTANCIA ACHALA"),
  (u'S3060', u"ESTANCIA LA CIGUEÑA"),
  (u'S3040XAE', u"ESTANCIA LA CONSTANCIA"),
  (u'S2105XAF', u"ESTANCIA LA MARÍA"),
  (u'S3057XAC', u"ESTANCIA LAS GAMAS"),
  (u'S3057XAD', u"ESTANCIA LOS PALMARES"),
  (u'S3057XAE', u"ESTANCIA PAVENHAN"),
  (u'S3040XAF', u"ESTANCIA PRUSIA"),
  (u'S2107XAA', u"ESTANCIA SAN ANTONIO"),
  (u'S2344XAD', u"ESTANCIA SAN FRANCISCO"),
  (u'S3066', u"ESTEBAN RAMS"),
  (u'S3036XAE', u"ESTHER"),
  (u'S2409XAB', u"ESTRADA"),
  (u'S2407XAE', u"EUSTOLIA"),
  (u'S3561XAD', u"EWALD"),
  (u'S2156XAA', u"FABRICA MILITAR SAN LORENZO"),
  (u'S2300XAC', u"FASSI"),
  (u'S3087', u"FELICIA"),
  (u'S2301', u"FIDELA"),
  (u'S2126', u"FIGHIERA"),
  (u'S2630', u"FIRMAT"),
  (u'S3054XAA', u"FIVES LILLE"),
  (u'S3575XAJ', u"FLOR DE ORO"),
  (u'S3516', u"FLORENCIA"),
  (u'S3565XAB', u"FLORIDA"),
  (u'S3066XAA', u"FORTIN ALERTA"),
  (u'S3046', u"FORTIN ALMAGRO"),
  (u'S3060XAA', u"FORTIN ARGENTINA"),
  (u'S3061XAA', u"FORTÍN ATAHUALPA"),
  (u'S3060XAB', u"FORTÍN CACIQUE"),
  (u'S3060XAP', u"FORTÍN CHARRUA"),
  (u'S3553XAH', u"FORTÍN CHILCAS"),
  (u'S3553', u"FORTÍN OLMOS"),
  (u'S3061XAB', u"FORTIN SEIS DE CABALLERIA"),
  (u'S3060XAL', u"FORTÍN TACURÚ"),
  (u'S3060XAC', u"FORTIN TOSTADO"),
  (u'S2111XAA', u"FRANCISCO PAZ"),
  (u'S3009', u"FRANCK"),
  (u'S2156', u"FRAY LUÍS BELTRÁN"),
  (u'S2438', u"FRONTERA"),
  (u'S2123', u"FUENTES"),
  (u'S2132', u"FUNES"),
  (u'S2208', u"GABOTO"),
  (u'S2307XAB', u"GALISTEO"),
  (u'S2252', u"GÁLVEZ"),
  (u'S3551XAS', u"GARABATO"),
  (u'S2443XAB', u"GARIBALDI"),
  (u'S3541', u"GATO COLORADO"),
  (u'S2701', u"GENERAL GELLY"),
  (u'S2126', u"GENERAL LAGOS"),
  (u'S2253', u"GESSLER"),
  (u'S3044', u"GOBERNADOR CRESPO"),
  (u'S2639', u"GÖDEKEN"),
  (u'S2921', u"GODOY"),
  (u'S3551', u"GOLONDRINA"),
  (u'S2132XAD', u"GRANADERO B BARGAS"),
  (u'S2152', u"GRANADERO BAIGORRIA"),
  (u'S2257XAA', u"GRANADERO BRASILIO BUSTOS"),
  (u'S2156XAD', u"GRANADEROS"),
  (u'S2501XAD', u"GRANJA SAN MANUEL"),
  (u'S3061', u"GREGORIA PÉREZ DE DENIS"),
  (u'S3083', u"GRÜTLY"),
  (u'S3083', u"GRÜTLY NORTE"),
  (u'S3574XAB', u"GUADALUPE NORTE"),
  (u'S3054XAC', u"GUARANIES"),
  (u'S3581XAA', u"GUASUNCHO"),
  (u'S3551XAO', u"GUAYCURÚ"),
  (u'S3003', u"HELVECIA"),
  (u'S2352', u"HERSILIA"),
  (u'S3023', u"HIPATÍA"),
  (u'S3076', u"HUANQUEROS"),
  (u'S2317XAE', u"HUGENTOBLER"),
  (u'S2344XAB', u"HUGENTOBLER"),
  (u'S2725', u"HUGHES"),
  (u'S2309', u"HUMBERTO PRIMERO"),
  (u'S3081', u"HUMBOLDT"),
  (u'S3081XAB', u"HUMBOLDT CHICO"),
  (u'S2142', u"IBARLUCEA"),
  (u'S3060XAD', u"INDEPENDENCIA"),
  (u'S3023XAD', u"INGENIERO BOASI"),
  (u'S3575XAB', u"INGENIERO CHANOURDIE"),
  (u'S3586XAA', u"INGENIERO GARMENDIA"),
  (u'S3586XAB', u"INGENIERO GERMANIA"),
  (u'S3551', u"INTIYACO"),
  (u'S2248', u"IRIGOYEN"),
  (u'S3018XAA', u"IRIONDO"),
  (u'S3001', u"ISLA DEL PORTEÑO"),
  (u'S3583XAA', u"ISLA TIGRE"),
  (u'S3581XAB', u"ISLETA"),
  (u'S2521', u"ITURRASPE"),
  (u'S2311XAE', u"ITUZAINGÓ"),
  (u'S3029', u"JACINTO L ARAUZ"),
  (u'S2204XAA', u"JESÚS MARÍA"),
  (u'S3041XAA', u"JOSÉ MACIAS"),
  (u'S2403XAC', u"JOSÉ MANUEL ESTRADA"),
  (u'S2103', u"JUAN B MOLINA"),
  (u'S2154XAA', u"JUAN ORTÍZ"),
  (u'S2723', u"JUNCAL"),
  (u'S2407XAD', u"KILOMETRO 113"),
  (u'S3565XAE', u"KILOMETRO 17"),
  (u'S3050XAA', u"KILÓMETRO 213"),
  (u'S3589XAA', u"KILÓMETRO 23"),
  (u'S3076XAC', u"KILOMETRO 235"),
  (u'S3014XAH', u"KILOMETRO 28"),
  (u'S3066XAD', u"KILOMETRO 293"),
  (u'S3565XAF', u"KILOMETRO 30"),
  (u'S3551', u"KILOMETRO 302"),
  (u'S2154XAB', u"KILOMETRO 319"),
  (u'S3551XAE', u"KILOMETRO 320"),
  (u'S2142XAB', u"KILOMETRO 323"),
  (u'S3014XAI', u"KILOMETRO 35"),
  (u'S3061XAE', u"KILOMETRO 389"),
  (u'S3551XAF', u"KILOMETRO 392"),
  (u'S6106XAB', u"KILOMETRO 396"),
  (u'S3585XAB', u"KILOMETRO 403"),
  (u'S3580XAB', u"KILOMETRO 408"),
  (u'S3581', u"KILOMETRO 41"),
  (u'S3020XAB', u"KILOMETRO 41"),
  (u'S3585XAC', u"KILOMETRO 421"),
  (u'S3061XAF', u"KILOMETRO 421"),
  (u'S2454XAA', u"KILOMETRO 443"),
  (u'S2456XAB', u"KILOMETRO 465"),
  (u'S3061XAG', u"KILOMETRO 468"),
  (u'S2456XAA', u"KILOMETRO 483"),
  (u'S2506XAA', u"KILOMETRO 49"),
  (u'S3023XAB', u"KILOMETRO 49"),
  (u'S3589XAE', u"KILOMETRO 49"),
  (u'S2438', u"KILOMETRO 501"),
  (u'S3589XAF', u"KILOMETRO 54"),
  (u'S3581XAC', u"KILOMETRO 67"),
  (u'S2303XAA', u"KILOMETRO 85"),
  (u'S3000XAE', u"KILÓMETRO 9"),
  (u'S3046XAG', u"KILÓMETRO 95"),
  (u'S6103XAA', u"LA ADELAIDA"),
  (u'S6106XAC', u"LA ASTURIANA"),
  (u'S3551XAB', u"LA BLANCA"),
  (u'S3060XAJ', u"LA BOMBILLA"),
  (u'S3045XAC', u"LA BRAVA"),
  (u'S3074', u"LA CABRAL"),
  (u'S2520XAC', u"LA CALIFORNIA"),
  (u'S6106XAD', u"LA CALMA"),
  (u'S3054XAB', u"LA CAMILA"),
  (u'S3040XAH', u"LA CAPILLA"),
  (u'S2105XAA', u"LA CAROLINA"),
  (u'S3572XAG', u"LA CATALINA"),
  (u'S2115XAB', u"LA CELIA"),
  (u'S3569XAD', u"LA CELIA"),
  (u'S2000XAA', u"LA CERAMICA Y CUYO"),
  (u'S2601', u"LA CHISPA"),
  (u'S3057', u"LA CIGUEÑA"),
  (u'S3025XAB', u"LA CLARA"),
  (u'S3585XAA', u"LA CLARITA"),
  (u'S3021XAE', u"LA CLORINDA"),
  (u'S6103XAB', u"LA CONSTANCIA"),
  (u'S3052', u"LA CRIOLLA"),
  (u'S3569XAE', u"LA DIAMELA"),
  (u'S2341XAB', u"LA ELSA"),
  (u'S3560XAA', u"LA ESMERALDA"),
  (u'S3057', u"LA GALLARETA"),
  (u'S2615XAA', u"LA GAMA"),
  (u'S3056XAD', u"LA GUAMPITA"),
  (u'S3001XAS', u"LA GUARDIA"),
  (u'S3050XAB', u"LA HOSCA"),
  (u'S6100XAA', u"LA INÉS"),
  (u'S2601XAA', u"LA INGLESITA"),
  (u'S3565XAC', u"LA JOSEFINA"),
  (u'S3046XAN', u"LA JULIA"),
  (u'S2126XAC', u"LA LATA"),
  (u'S3567XAA', u"LA LOLA"),
  (u'S3555XAC', u"LA LOMA"),
  (u'S3072XAC', u"LA LUCILA"),
  (u'S2341XAC', u"LA MARINA"),
  (u'S2173XAB', u"LA MERCED"),
  (u'S2613XAA', u"LA MOROCHA"),
  (u'S3001XAJ', u"LA NORIA"),
  (u'S3054XAG', u"LA ORIENTAL"),
  (u'S3080XAC', u"LA ORILLA"),
  (u'S2115XAA', u"LA OTHILA"),
  (u'S3027', u"LA PELADA"),
  (u'S6036XAA', u"LA PICASA"),
  (u'S3074XAE', u"LA POLVAREDA"),
  (u'S3563XAC', u"LA POTASA"),
  (u'S3581XAD', u"LA RESERVA"),
  (u'S3042XAD', u"LA ROSA"),
  (u'S2342', u"LA RUBIA"),
  (u'S2142', u"LA SALADA"),
  (u'S3563XAF', u"LA SARITA"),
  (u'S3057XAF', u"LA SARNOSA"),
  (u'S3551XAG', u"LA SELVA"),
  (u'S3038XAA', u"LA SEMENTERA"),
  (u'S2105', u"LA VANGUARDIA"),
  (u'S3561XAE', u"LA VANGUARDIA"),
  (u'S3076XAA', u"LA VERDE"),
  (u'S2183XAA', u"LA VIUDA"),
  (u'S3551XAH', u"LA ZULEMA"),
  (u'S2726', u"LABORDEBOY"),
  (u'S3020', u"LAGUNA PAIVA"),
  (u'S3076XAB', u"LAGUNA VERDE"),
  (u'S2531', u"LANDETA"),
  (u'S3575', u"LANTERI"),
  (u'S2144XAC', u"LARGUÍA"),
  (u'S2241', u"LARRECHEA"),
  (u'S3080XAD', u"LARRECHEA"),
  (u'S3560XAD', u"LAS ANINTAS"),
  (u'S3060XAM', u"LAS ARENAS"),
  (u'S3074XAD', u"LAS AVISPAS"),
  (u'S2148', u"LAS BANDURRIAS"),
  (u'S3046', u"LAS CAÑAS"),
  (u'S3560XAE', u"LAS CATALINAS"),
  (u'S3061', u"LAS CHUÑAS"),
  (u'S3551XAI', u"LAS DELICIAS"),
  (u'S6106XAG', u"LAS DOS ANGELITAS"),
  (u'S2607XAC', u"LAS ENCADENADAS"),
  (u'S3560XAH', u"LAS GARSITAS"),
  (u'S3574', u"LAS GARZAS"),
  (u'S3013XAC', u"LAS HIGUERITAS"),
  (u'S2520XAD', u"LAS LIEBRES"),
  (u'S3516XAD', u"LAS MERCEDES"),
  (u'S3555XAA', u"LAS PALMAS"),
  (u'S2326XAD', u"LAS PALMERAS"),
  (u'S2505', u"LAS PAREJAS"),
  (u'S2451', u"LAS PETACAS"),
  (u'S2200XAB', u"LAS QUINTAS"),
  (u'S2520', u"LAS ROSAS"),
  (u'S3575XAC', u"LAS SIETE PROVINCIAS"),
  (u'S3586', u"LAS TOSCAS"),
  (u'S3046XAB', u"LAS TRES MARÍAS"),
  (u'S2500XAB', u"LAS TROJAS"),
  (u'S3009', u"LAS TUNAS"),
  (u'S3036XAC', u"LASSAGA"),
  (u'S6103XAD', u"LAZZARINO"),
  (u'S2305', u"LEHMANN"),
  (u'S2132XAA', u"LICEO AERONAUTICO MILITAR"),
  (u'S2132XAB', u"LINKS"),
  (u'S3036', u"LLAMBÍ CAMPBELL"),
  (u'S3066', u"LOGROÑO"),
  (u'S2253', u"LOMA ALTA"),
  (u'S2117XAA', u"LOMA VERDE"),
  (u'S2255', u"LÓPEZ"),
  (u'S3551XAT', u"LOS AMORES"),
  (u'S2720XAB', u"LOS ARCOS"),
  (u'S3005XAD', u"LOS CARDENALES"),
  (u'S2533', u"LOS CARDOS"),
  (u'S3001XAK', u"LOS CERRILLOS"),
  (u'S3060XAK', u"LOS CHARABONES"),
  (u'S3551XAC', u"LOS CLAROS"),
  (u'S3051XAB', u"LOS CORRALITOS"),
  (u'S3555XAD', u"LOS CUERVOS"),
  (u'S3050XAC', u"LOS GALPONES"),
  (u'S3021XAB', u"LOS HORNOS"),
  (u'S3575XAD', u"LOS LAPACHOS"),
  (u'S3567', u"LOS LAURELES"),
  (u'S3551XAD', u"LOS LEONES"),
  (u'S2146XAA', u"LOS LEONES"),
  (u'S2181', u"LOS MOLINOS"),
  (u'S3070XAB', u"LOS MOLLES"),
  (u'S2105XAB', u"LOS MUCHACHOS"),
  (u'S2183', u"LOS NOGALES"),
  (u'S3046XAO', u"LOS OLIVOS"),
  (u'S3051XAC', u"LOS OSOS"),
  (u'S3057XAG', u"LOS PALMARES"),
  (u'S2637', u"LOS QUIRQUINCHOS"),
  (u'S3041XAC', u"LOS SALADILLOS"),
  (u'S2447XAA', u"LOS SEMBRADOS"),
  (u'S3551XAU', u"LOS TABANOS DESVIO KM 366"),
  (u'S3048XAE', u"LUCIANO LEIVA"),
  (u'S2142', u"LUCIO V LÓPEZ"),
  (u'S2142XAC', u"LUIS PALACIOS"),
  (u'S2208', u"MACIEL"),
  (u'S2622', u"MAGGIOLO"),
  (u'S2119XAC', u"MAIZALES"),
  (u'S3572', u"MALABRIGO"),
  (u'S2445XAB', u"MANGORÉ"),
  (u'S3023XAA', u"MANUCHO"),
  (u'S3042', u"MARCELINO ESCALADA"),
  (u'S3056', u"MARGARITA"),
  (u'S3072XAA', u"MARÍA EUGENIA"),
  (u'S2445', u"MARÍA JUANA"),
  (u'S3025', u"MARIA LUISA"),
  (u'S2501', u"MARIA LUISA CORREA"),
  (u'S2527', u"MARÍA SUSANA"),
  (u'S2609', u"MARÍA TERESA"),
  (u'S3011', u"MARIANO SAAVEDRA"),
  (u'S2301', u"MARINI"),
  (u'S3041XAE', u"MASCIAS"),
  (u'S2115', u"MÁXIMO PAZ"),
  (u'S2728', u"MELINCUÉ"),
  (u'S2725XAA', u"MERCEDITAS"),
  (u'S3046XAP', u"MIGUEL ESCALADA"),
  (u'S2631', u"MIGUEL TORRES"),
  (u'S6106XAI', u"MIRAMAR"),
  (u'S3581XAE', u"MOCOVÍ"),
  (u'S2313', u"MOISÉS VILLE"),
  (u'S2342', u"MONIGOTES"),
  (u'S2212', u"MONJE"),
  (u'S2101XAA', u"MONTE FLORES"),
  (u'S2349XAB', u"MONTE OBSCURIDAD"),
  (u'S3014', u"MONTE VERA"),
  (u'S2521', u"MONTES DE OCA"),
  (u'S3561XAB', u"MOUSSY"),
  (u'S2601', u"MURPHY"),
  (u'S2313XAE', u"MUTCHNIK"),
  (u'S3046XAH', u"NARÉ"),
  (u'S3032', u"NELSON"),
  (u'S3563XAD', u"NICANOR E MOLINAS"),
  (u'S3074XAA', u"NUEVA ITALIA"),
  (u'S3014XAC', u"NUEVA POMPEYA"),
  (u'S3046XAI', u"NUEVA UKRANIA"),
  (u'S3087', u"NUEVO TORINO"),
  (u'S3553', u"ÑANDU"),
  (u'S3041', u"ÑANDUBAY"),
  (u'S3072', u"ÑANDUCITA"),
  (u'S3589XAB', u"OBRAJE INDIO MUERTO"),
  (u'S3589XAC', u"OBRAJE SAN JUAN"),
  (u'S3551', u"OGILVIE"),
  (u'S2206', u"OLIVEROS"),
  (u'S3005XAH', u"OMBU NORTE"),
  (u'S2921XAB', u"ORATORIO MORANTE"),
  (u'S2253', u"OROÑO"),
  (u'S2605XAA', u"OTTO BEMBERG"),
  (u'S3061XAJ', u"PADRE PEDRO ITURRALDE"),
  (u'S2152XAA', u"PAGANINI"),
  (u'S3046XAJ', u"PAIKÍN"),
  (u'S2326XAB', u"PALACIOS"),
  (u'S3553', u"PARAJE 29"),
  (u'S3550XAB', u"PARAJE KILOMETRO 12"),
  (u'S3551XAP', u"PARAJE TRAGNAGHI"),
  (u'S3080XAA', u"PASO VINAL"),
  (u'S3585XAD', u"PAUL GROUSSAC"),
  (u'S3057XAB', u"PAVENHAN"),
  (u'S2918', u"PAVÓN"),
  (u'S2109', u"PAVÓN ARRIBA"),
  (u'S3054XAD', u"PEDRO GÓMEZ CELLO"),
  (u'S2105XAC', u"PEREYRA LUCENA"),
  (u'S2121', u"PÉREZ"),
  (u'S3025', u"PERICOTA"),
  (u'S3046XAD', u"PETRONILA"),
  (u'S2113', u"PEYRANO"),
  (u'S2529', u"PIAMONTE"),
  (u'S3085', u"PILAR"),
  (u'S2200XAC', u"PINO DE SAN LORENZO"),
  (u'S2119', u"PIÑERO"),
  (u'S3000XAA', u"PIQUETE"),
  (u'S3014XAD', u"POMPEYA"),
  (u'S3066XAE', u"PORTALIS"),
  (u'S3071XAB', u"PORTUGALETE"),
  (u'S3589XAD', u"POTRERO GUASUNCHO"),
  (u'S3061', u"POZO BORRADO"),
  (u'S3551XAQ', u"POZO DE LOS INDIOS"),
  (u'S2301XAD', u"PRESIDENTE ROCA"),
  (u'S3023', u"PROGRESO"),
  (u'S3025', u"PROVIDENCIA"),
  (u'S3080XAE', u"PUEBLO ABC"),
  (u'S2183', u"PUEBLO AREQUITO"),
  (u'S3000XAF', u"PUEBLO CANDIOTI"),
  (u'S2126', u"PUEBLO ESTHER"),
  (u'S3551XAJ', u"PUEBLO GOLONDRINA"),
  (u'S2202XAD', u"PUEBLO KIRSTON"),
  (u'S2445', u"PUEBLO MARIA JUANA"),
  (u'S2119', u"PUEBLO MUÑOZ"),
  (u'S2124XAA', u"PUEBLO NUEVO"),
  (u'S2301', u"PUEBLO SAN ANTONIO"),
  (u'S2300XAA', u"PUEBLO TERRAGNI"),
  (u'S2242XAB', u"PUENTE COLASTINE"),
  (u'S2246XAA', u"PUERTO ARAGÓN"),
  (u'S2200XAA', u"PUERTO DE SAN LORENZO"),
  (u'S2208XAA', u"PUERTO GABOTO"),
  (u'S2202', u"PUERTO GRAL SAN MARTIN"),
  (u'S3580XAC', u"PUERTO OCAMPO"),
  (u'S3516XAE', u"PUERTO PIRACUÁ"),
  (u'S3592XAC', u"PUERTO PIRACUACITO"),
  (u'S3567XAC', u"PUERTO RECONQUISTA"),
  (u'S2123', u"PUJATO"),
  (u'S3080XAF', u"PUJATO NORTE"),
  (u'S2600XAE', u"RABIOLA"),
  (u'S2300', u"RAFAELA"),
  (u'S3042', u"RAMAYÓN"),
  (u'S2301', u"RAMONA"),
  (u'S2322XAB', u"RAQUEL"),
  (u'S2605XAB', u"RASTREADOR FOURNIER"),
  (u'S3560', u"RECONQUISTA"),
  (u'S3018', u"RECREO"),
  (u'S3001XAL', u"RECREO SUR"),
  (u'S2309XAB', u"REINA MARGARITA"),
  (u'S3020XAC', u"REYNALDO CULLEN"),
  (u'S2201', u"RICARDONE"),
  (u'S2255XAB', u"RIGBY"),
  (u'S2206XAB', u"RINCON DE GRONDONA"),
  (u'S3046XAE', u"RINCON DE SAN ANTONIO"),
  (u'S2317XAA', u"RINCON DE TACURALES"),
  (u'S3080XAG', u"RINCÓN DEL PINTADO"),
  (u'S3025XAC', u"RINCON DEL QUEBRACHO"),
  (u'S3001XAT', u"RINCON NORTE"),
  (u'S3001XAU', u"RINCON POTREROS"),
  (u'S3023XAC', u"RINLON DE AVILA"),
  (u'S3036XAD', u"RÍO SALADO"),
  (u'S3081XAC', u"RIVADAVIA"),
  (u'S2115XAC', u"RODOLFO ALCORTA"),
  (u'S2134', u"ROLDÁN"),
  (u'S3555', u"ROMANG"),
  (u'S2000', u"ROSARIO"),
  (u'S2921', u"RUEDA"),
  (u'S6100', u"RUFINO"),
  (u'S3001XAF', u"RUINAS SANTA FE LA VIEJA"),
  (u'S2611XAA', u"RUNCIMAN"),
  (u'S3011', u"SA PEREYRA"),
  (u'S2301', u"SAGUIER"),
  (u'S3001XAX', u"SALADERO M CABAL"),
  (u'S2142', u"SALTO GRANDE"),
  (u'S3017', u"SAN AGUSTÍN"),
  (u'S3565XAD', u"SAN ALBERTO"),
  (u'S3587XAA', u"SAN ANTONIO DE OBLIGADO"),
  (u'S3048, S3061XAL', u"SAN BERNARDO"),
  (u'S6106XAH', u"SAN CARLOS"),
  (u'S3013', u"SAN CARLOS CENTRO"),
  (u'S3009', u"SAN CARLOS NORTE"),
  (u'S3013', u"SAN CARLOS SUD"),
  (u'S3070', u"SAN CRISTÓBAL"),
  (u'S2615', u"SAN EDUARDO"),
  (u'S2501XAA', u"SAN ESTANISLAO"),
  (u'S2253', u"SAN EUGENIO"),
  (u'S2242', u"SAN FABIÁN"),
  (u'S2601', u"SAN FRANCISCO DE SANTA FE"),
  (u'S2146', u"SAN GENARO"),
  (u'S2147', u"SAN GENARO NORTE"),
  (u'S2136XAA', u"SAN GERÓNIMO"),
  (u'S2613', u"SAN GREGORIO"),
  (u'S2512XAA', u"SAN GUILLERMO"),
  (u'S3020XAD', u"SAN GUILLERMO"),
  (u'S2347', u"SAN GUILLERMO"),
  (u'S3005', u"SAN JAVIER"),
  (u'S3009', u"SAN JERÓNIMO DEL SAUCE"),
  (u'S3011', u"SAN JERÓNIMO NORTE"),
  (u'S2136', u"SAN JERÓNIMO SUR"),
  (u'S3001XAG', u"SAN JOAQUÍN"),
  (u'S2451', u"SAN JORGE"),
  (u'S3016', u"SAN JOSÉ"),
  (u'S2185', u"SAN JOSÉ DE LA ESQUINA"),
  (u'S3001', u"SAN JOSÉ DEL RINCÓN"),
  (u'S2401XAB', u"SAN JOSÉ FRONTERA"),
  (u'S3040', u"SAN JUSTO"),
  (u'S2200', u"SAN LORENZO"),
  (u'S6009XAA', u"SAN MARCELO"),
  (u'S2600XAA', u"SAN MARCOS DE VENADO TUERTO"),
  (u'S3011XAA', u"SAN MARIANO"),
  (u'S2449', u"SAN MARTÍN DE LAS ESCOBAS"),
  (u'S2255XAC', u"SAN MARTÍN DE TOURS"),
  (u'S3045XAD', u"SAN MARTÍN NORTE"),
  (u'S2309XAC', u"SAN MIGUEL"),
  (u'S3021XAC', u"SAN PEDRO"),
  (u'S3021XAD', u"SAN PEDRO NORTE"),
  (u'S3014XAE', u"SAN PEDRO SUR"),
  (u'S2501XAB', u"SAN RICARDO"),
  (u'S3553XAA', u"SAN ROQUE"),
  (u'S2121XAC', u"SAN SEBASTIÁN"),
  (u'S2728XAA', u"SAN URBANO"),
  (u'S2447', u"SAN VICENTE"),
  (u'S3580XAA', u"SAN VICENTE"),
  (u'S2617', u"SANCTI SPÍRITU"),
  (u'S2173', u"SANFORD"),
  (u'S3575XAE', u"SANTA ANA"),
  (u'S2258XAA', u"SANTA CLARA"),
  (u'S2258', u"SANTA CLARA DE BUENA VISTA"),
  (u'S2405', u"SANTA CLARA DE SAGUIER"),
  (u'S2725XAB', u"SANTA EMILIA"),
  (u'S2317', u"SANTA EUSEBIA"),
  (u'S3000', u"SANTA FE"),
  (u'S3551', u"SANTA FELICIA"),
  (u'S2605', u"SANTA ISABEL"),
  (u'S3553XAF', u"SANTA LUCÍA"),
  (u'S3061', u"SANTA MARGARITA"),
  (u'S3011XAB', u"SANTA MARÍA"),
  (u'S2639XAJ', u"SANTA NATALIA"),
  (u'S6106XAJ', u"SANTA PAULA"),
  (u'S3001', u"SANTA ROSA DE CALCHINES"),
  (u'S2111', u"SANTA TERESA"),
  (u'S6106XAK', u"SANTA TERESA"),
  (u'S3025XAA', u"SANTO DOMINGO"),
  (u'S3016', u"SANTO TOME"),
  (u'S3074XAF', u"SANTURCE"),
  (u'S2105', u"SARGENTO CABRAL"),
  (u'S3023', u"SARMIENTO"),
  (u'S2440', u"SASTRE"),
  (u'S3017', u"SAUCE VIEJO"),
  (u'S2451XAC', u"SCHIFFNER"),
  (u'S2138XAB', u"SEMINO"),
  (u'S2216', u"SERODINO"),
  (u'S3014XAF', u"SETUBAL"),
  (u'S2300XAE', u"SIERRA PEREYRA"),
  (u'S3060XAO', u"SIN PEREZA"),
  (u'S3048', u"SOL DE MAYO"),
  (u'S2107', u"SOLDINI"),
  (u'S3025XAE', u"SOLEDAD"),
  (u'S3025XAF', u"SOUTO MAYOR"),
  (u'S2103XAA', u"STEPHENSON"),
  (u'S2349', u"SUARDI"),
  (u'S2322', u"SUNCHALES"),
  (u'S2301', u"SUSANA"),
  (u'S3587', u"TACUARENDÍ"),
  (u'S2324', u"TACURAL"),
  (u'S2535XAA', u"TAIS"),
  (u'S2121XAD', u"TALLERES"),
  (u'S6103XAE', u"TARRAGONA"),
  (u'S3565XAG', u"TARTAGAL"),
  (u'S6009', u"TEODELINA"),
  (u'S2918', u"THEOBALD"),
  (u'S2204', u"TIMBUES JOSÉ MARIA"),
  (u'S3551XAR', u"TOBA"),
  (u'S3023XAF', u"TOMÁS ALVA EDISON"),
  (u'S2512', u"TORTUGAS"),
  (u'S3060', u"TOSTADO"),
  (u'S2144', u"TOTORAS"),
  (u'S2456XAC', u"TRAILL"),
  (u'S3560XAG', u"TRES BOCAS"),
  (u'S2300XAF', u"TRES COLONIAS"),
  (u'S2921XAA', u"TRES ESQUINAS"),
  (u'S3061XAK', u"TRES POZOS"),
  (u'S2156XAE', u"TTE HIPOLITO BOUCHARD"),
  (u'S2105', u"URANGA"),
  (u'S2313XAF', u"VEINTICUATRO CASAS"),
  (u'S3550XAC', u"VELAZQUEZ"),
  (u'S2600', u"VENADO TUERTO"),
  (u'S3550', u"VERA"),
  (u'S3040XAD', u"VERA MUJICA"),
  (u'S3054XAE', u"VERA Y PINTADO"),
  (u'S2142XAD', u"VICENTE ECHEVARRIA"),
  (u'S3563XAE', u"VICTOR MANUEL SEGUNDO"),
  (u'S3048', u"VIDELA"),
  (u'S2301', u"VILA"),
  (u'S3581', u"VILLA ADELA"),
  (u'S2101', u"VILLA AMELIA"),
  (u'S2121XAA', u"VILLA AMÉRICA"),
  (u'S3583', u"VILLA ANA"),
  (u'S2147XAA', u"VILLA BIOTA"),
  (u'S2607', u"VILLA CAÑAS"),
  (u'S2154XAC', u"VILLA CASSINI"),
  (u'S2919', u"VILLA CONSTITUCIÓN"),
  (u'S2631XAC', u"VILLA DIVISA DE MAYO"),
  (u'S3000XAB', u"VILLA DON BOSCO"),
  (u'S2503', u"VILLA ELOÍSA"),
  (u'S2726XAA', u"VILLA ESTELA"),
  (u'S2630XAB', u"VILLA FREDICKSON"),
  (u'S2156XAF', u"VILLA GARIBALDI"),
  (u'S2124', u"VILLA GOBERNADOR GÁLVEZ"),
  (u'S2148XAA', u"VILLA GUASTALLA"),
  (u'S3589', u"VILLA GUILLERMINA"),
  (u'S2500XAC', u"VILLA LA RIBERA"),
  (u'S3042XAE', u"VILLA LASTENIA"),
  (u'S3016XAA', u"VILLA LUJÁN"),
  (u'S2121XAB', u"VILLA LYLY TALLERES"),
  (u'S2156XAG', u"VILLA MARGARITA"),
  (u'S3000XAC', u"VILLA MARIA SELVA"),
  (u'S3061', u"VILLA MINETTI"),
  (u'S2175', u"VILLA MUGUETA"),
  (u'S3580', u"VILLA OCAMPO"),
  (u'S2123XAC', u"VILLA PORUCCI"),
  (u'S2630XAA', u"VILLA REGULES"),
  (u'S6100XAB', u"VILLA ROSELLO"),
  (u'S2124XAC', u"VILLA SAN DIEGO"),
  (u'S2301', u"VILLA SAN JOSÉ"),
  (u'S3046XAF', u"VILLA SARALEGUI"),
  (u'S2345', u"VILLA TRINIDAD"),
  (u'S3001XAV', u"VILLA VIVEROS"),
  (u'S3000XAH', u"VILLA YAPEYU"),
  (u'S2173', u"VILLADA"),
  (u'S2400XAA', u"VILLANI"),
  (u'S2311XAD', u"VIRGINIA"),
  (u'S3001', u"VUELTA DEL PIRATA"),
  (u'S2313XAA', u"WALVELBERG"),
  (u'S2722', u"WHEELWRIGHT"),
  (u'S2257XAB', u"WILDERMUTH"),
  (u'S3586XAD', u"YAGUARETÉ"),
  (u'S3014XAJ', u"YAMANDU"),
  (u'S2326XAC', u"ZADOCKHAN"),
  (u'S2105XAD', u"ZAMPONI"),
  (u'S2301XAF', u"ZANETTI"),
  (u'S2123', u"ZAVALLA"),
  (u'S2409', u"ZENÓN PEREYRA"),
)

CP_dict = dict(CP)

def solic(request, eid=None, domfiscal=None, localidad=None, cp=None):
    e = get_object_or_404(Expediente, id=eid)
    return render_to_response('solic.html', {"e": e, "domfiscal": domfiscal, "localidad": localidad, "cp": cp}, context_instance=RequestContext(request))

class SolicitudForm(forms.Form):
    expte_nro = forms.IntegerField()
    domicilio_fiscal = forms.CharField(max_length=40)
    localidad = forms.ChoiceField(choices=CP, initial='S2252')

def solic_form(request):
    if request.method == 'POST': # If the form has been submitted...
        # SolicitudForm was defined in the previous section
        form = SolicitudForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            expediente_id = form.cleaned_data['expte_nro']
            domicilio_fiscal = form.cleaned_data['domicilio_fiscal']
            codigo_postal = form.cleaned_data['localidad']
            localidad = CP_dict[codigo_postal]

            return HttpResponseRedirect('/gea/solic/%s/%s/%s/%s' % (expediente_id, domicilio_fiscal, localidad, codigo_postal)) # Redirect after POST
    else:
        form = SolicitudForm() # An unbound form

    return render(request, 'solic_form.html', {
        'form': form,
    })

#
# Visacion Comunal/Municipal
#

LUGAR = (
  (0, u'GÁLVEZ'),
  (1, u'AROCENA'),
  (2, u'BARRANCAS'),
  (3, u'BERNARDO DE IRIGOYEN'),
  (4, u'CAMPO PIAGGIO'),
  (5, u'CARRIZALES'),
  (6, u'CASALEGNO'),
  (7, u'COLONIA BELGRANO'),
  (8, u'CORONDA'),
  (9, u'DÍAZ'),
  (10, u'GABOTO'),
  (11, u'GESSLER'),
  (12, u'IRIGOYEN'),
  (13, u'LARRECHEA'),
  (14, u'LOMA ALTA'),
  (15, u'LÓPEZ'),
  (16, u'MACIEL'),
  (17, u'MATILDE'),
  (18, u'MONJE'),
  (19, u'OLIVEROS'),
  (20, u'SAN CARLOS CENTRO'),
  (21, u'SAN EUGENIO'),
  (22, u'SAN FABIÁN'),
  (23, u'SAN GENARO'),
  (24, u'SAN MARIANO'),
  (25, u'SAN MARTÍN DE LAS ESCOBAS'),
  (26, u'SANTA CLARA DE BUENA VISTA'),
)

Lugar_dict = {
  0: (u'Sr. Secretario de Obras, Servicios Públicos y Gestión', u'MUNICIPALIDAD DE GÁLVEZ'),
  1: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO AROCENA'),
  2: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO BARRANCAS'),
  3: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO BERNARDO DE IRIGOYEN'),
  4: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO CAMPO PIAGGIO'),
  5: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO CARRIZALES'),
  6: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO CASALEGNO'),
  7: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO COLONIA BELGRANO'),
  8: (u'Sr. Secretario de Obras y Servicios Públicos', u'MUNICIPALIDAD DE CORONDA'),
  9: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO ESTACIÓN DÍAZ'),
  10: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO GABOTO'),
  11: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO GESSLER'),
  12: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO IRIGOYEN'),
  13: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO LARRECHEA'),
  14: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO LOMA ALTA'),
  15: (u'Sra. Presidenta de la Comisión Comunal de', u'PUEBLO LÓPEZ'),
  16: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO MACIEL'),
  17: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO MATILDE'),
  18: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO MONJE'),
  19: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO OLIVEROS'),
  20: (u'Sr. Secretario de Obras y Servicios Públicos', u'MUNICIPALIDAD DE SAN CARLOS CENTRO'),
  21: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO SAN EUGENIO'),
  22: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO SAN FABIAN'),
  23: (u'Sr. Intendente Municipal', u'MUNICIPALIDAD DE SAN GENARO'),
  24: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO SAN MARIANO'),
  25: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO SAN MARTÍN DE LAS ESCOBAS'),
  26: (u'Sr. Presidente de la Comisión Comunal', u'PUEBLO SANTA CLARA DE BUENA VISTA'),
}

def visac(request, eid=None, sr=None, localidad=None):
    e = get_object_or_404(Expediente, id=eid)
    return render_to_response('visac.html', {"e": e, "sr": sr, "localidad": localidad}, context_instance=RequestContext(request))

class VisacionForm(forms.Form):
    expte_nro = forms.IntegerField()
    lugar = forms.ChoiceField(choices=LUGAR, initial=0)

def visac_form(request):
    if request.method == 'POST': # If the form has been submitted...
        # VisacionForm was defined in the previous section
        form = VisacionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            expediente_id = form.cleaned_data['expte_nro']
            lugar = form.cleaned_data['lugar']
            sr = Lugar_dict[int(lugar)][0]
            localidad = Lugar_dict[int(lugar)][1]

            return HttpResponseRedirect('/gea/visac/%s/%s/%s' % (expediente_id, sr, localidad)) # Redirect after POST
    else:
        form = VisacionForm() # An unbound form

    return render(request, 'visac_form.html', {
        'form': form,
    })

#
# Buscar Plano por Nro
#
def plano(request, circunscripcion=None, nro_inscripcion=None):
    return HttpResponseRedirect('%s/planos/%s/%s.pdf' % (ftp_url, circunscripcion, nro_inscripcion))
    
class PlanoForm(forms.Form):
    circunscripcion = forms.IntegerField(min_value=1, max_value=2, initial=1)
    nro_inscripcion = forms.IntegerField(min_value=1, max_value=999999)

def plano_form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PlanoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            circ = form.cleaned_data['circunscripcion']
            nro = form.cleaned_data['nro_inscripcion']
            return HttpResponseRedirect('/gea/plano/%d/%06d' % (circ, nro))
    else:
        form = PlanoForm() # An unbound form

    return render(request, 'plano_form.html', {
        'form': form,
    })

#
# Buscar Set de Datos por PII
#
def set(request, pii=None, sub_pii=None):
    return HttpResponseRedirect('%s/set/%s%s.pdf' % (ftp_url, pii, sub_pii))

class SetForm(forms.Form):
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(min_value=0, max_value=9999, initial=0)

def set_form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SetForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            pii = form.cleaned_data['partida']
            sub_pii = form.cleaned_data['sub_pii']
            return HttpResponseRedirect('/gea/set/%06d%04d' % (pii, sub_pii))
    else:
        form = SetForm() # An unbound form

    return render(request, 'set_form.html', {
        'form': form,
    })

#
# Calcular Digito Verificador de la PII
#
def dvapi(request, dv):
    return render_to_response('dvapi.html', {"dv": dv}, context_instance=RequestContext(request))

def get_dvapi(dp, ds, sd, pii, subpii):
    coef = '9731'
    _coef = coef + coef + coef + coef
    strpii = '%02d%02d%02d%06d%04d' % (dp, ds, sd, pii, subpii)
    suma = 0
    for i in range(0, len(strpii)):
        m = str(int(strpii[i]) * int(_coef[i]))
        suma += int(m[len(m) - 1])
    return (10 - (suma % 10)) % 10

def dvapi_form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DVAPIForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            dp = form.cleaned_data['dp']
            ds = form.cleaned_data['ds']
            sd = form.cleaned_data['sd']
            pii = form.cleaned_data['partida']
            sub_pii = form.cleaned_data['sub_pii']
            dv = get_dvapi(dp, ds, sd, pii, sub_pii)
            return HttpResponseRedirect('/gea/dvapi/%d' % dv)
    else:
        form = DVAPIForm() # An unbound form

    return render(request, 'dvapi_form.html', {
        'form': form,
    })

class DVAPIForm(forms.Form):
    dp = forms.IntegerField(min_value=1, max_value=19, initial=11)
    ds = forms.IntegerField(min_value=1, max_value=99, initial=8)
    sd = forms.IntegerField(min_value=0, max_value=99, initial=0)
    partida = forms.IntegerField(min_value=1, max_value=999999)
    sub_pii = forms.IntegerField(min_value=0, max_value=9999, initial=0)

#
#
# Presupuestos
#
#
from gea.models import Persona, Objeto, Lugar, Partida

def presup(request, persona=None, objeto=None):
    #p = get_object_or_404(Persona, =eid)
    return render_to_response('presup.html', {"persona": persona, "objeto": objeto}, context_instance=RequestContext(request))

class PresupForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), empty_label=None)
    objeto  = forms.ModelChoiceField(queryset=Objeto.objects.all(), empty_label=None)
    lugar   = forms.ModelChoiceField(queryset=Lugar.objects.all())
    partida = forms.ModelChoiceField(queryset=Partida.objects.all())
    monto   = forms.FloatField(required=False)

def presup_form(request):
    if request.method == 'POST': # If the form has been submitted...
        # VisacionForm was defined in the previous section
        form = PresupForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            persona = form.cleaned_data['persona']
            objeto  = form.cleaned_data['objeto']
            lugar   = form.cleaned_data['lugar']
            partida = form.cleaned_data['partida']
            monto   = form.cleaned_data['monto']

            return HttpResponseRedirect('/gea/presup/%s/%s' % (persona, objeto)) # Redirect after POST
    else:
        form = PresupForm() # An unbound form

    return render(request, 'presup_form.html', {
        'form': form,
    })

#
#
# Exptes x Catastro Local
#
#
from django.forms import ModelForm
from gea.models import CatastroLocal

# class CLForm(ModelForm):
    # class Meta:
        # model = CatastroLocal

class CLForm(forms.Form):
    lugar   = forms.ModelChoiceField(queryset=Lugar.objects.exclude(nombre__startswith='Colonia').exclude(nombre__startswith='Zona Rural').exclude(nombre__startswith='Zona de Islas'), required=False)
    seccion	 = forms.CharField(max_length=4, required=False)
    manzana	 = forms.CharField(max_length=4, required=False)
    parcela	 = forms.CharField(max_length=4, required=False)

def catastro_form(request):
    if request.method == 'POST': # If the form has been submitted...
        # VisacionForm was defined in the previous section
        form = CLForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            lugar    = form.cleaned_data['lugar']
            seccion  = form.cleaned_data['seccion']
            manzana  = form.cleaned_data['manzana']
            parcela  = form.cleaned_data['parcela']

            filtro = u'?'
            if lugar != None:
                filtro  = u'%s%s%s' % (filtro, u'&expedientelugar__lugar__nombre=', lugar)
            if seccion != '':
                filtro  = u'%s%s%s' % (filtro, u'&expedientelugar__catastrolocal__seccion=', seccion)
            if manzana != '':
                filtro  = u'%s%s%s' % (filtro, u'&expedientelugar__catastrolocal__manzana=', manzana)
            if parcela != '':
                filtro  = u'%s%s%s' % (filtro, u'&expedientelugar__catastrolocal__parcela=', parcela)
            return HttpResponseRedirect('/admin/gea/expediente/%s' % filtro) # Redirect after POST
    else:
        form =CLForm() # An unbound form

    return render(request, 'catastro_form.html', {
        'form': form,
    })
