const L = {
    map: jest.fn(() => ({
        setView: jest.fn(),
        fitBounds: jest.fn(),
        remove: jest.fn(),
    })),
    tileLayer: jest.fn(() => ({
        addTo: jest.fn(),
    })),
    icon: jest.fn(),
    marker: jest.fn(() => ({
        addTo: jest.fn(() => ({
            bindPopup: jest.fn(),
        })),
        remove: jest.fn(),
        setLatLng: jest.fn(),
        bindPopup: jest.fn(),
    })),
    polyline: jest.fn(() => ({
        addTo: jest.fn(),
        setLatLngs: jest.fn(),
        remove: jest.fn(),
    })),
    featureGroup: jest.fn(() => ({
        addLayer: jest.fn(),
        clearLayers: jest.fn(),
        addTo: jest.fn(),
    })),
};

export default L;