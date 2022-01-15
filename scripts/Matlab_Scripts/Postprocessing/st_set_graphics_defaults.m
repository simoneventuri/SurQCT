function [prev] = st_set_graphics_defaults(opts)
    if ~exist('opts', 'var')
        opts = struct();
    end
    prev = struct();

    st_set('LegendFontSizeMode', 'manual');
    st_set('LegendInterpreter', 'latex');
    st_set('LegendFontSize', 38);

    st_set('TextInterpreter', 'latex');
    st_set('LineLineWidth', 1.5);

    st_set('AxesTickLabelInterpreter', 'latex');
    st_set('AxesNextPlot', 'add');
    st_set('AxesFontSize', 50);

    st_set('FigurePaperPositionMode', 'manual');
    st_set('FigureVisible', 'on');
    st_set('FigurePaperUnits', 'inches');
    st_set('FigurePaperPosition', [0, 0, 10, 8]);
    st_set('FigurePaperSize', [10, 8]);

    for f = fieldnames(opts)'
        st_set(f{1}, opts.(f{1}));
    end

    function st_set(name, value)
        if isfield(opts, name)
            value = opts.(name);
            opts = rmfield(opts, name);
        end

        prev.(name) = get(0, sprintf('default%s', name));
        set(0, sprintf('default%s', name), value);
    end
end


