
import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { createSelector } from 'reselect'
import type { RootState } from './store'


// modes to switch some page related features
export const MODES = {
    NONE: "none",
    SPEC_RANKING: "spec_ranking",
    COMP_RANKING: "comp_ranking",
}

export type Mode = "none" | "spec_ranking" | "comp_ranking"



////////////////////////////////////////////////////////////////////////////////
// Actions
//
export function get_mode(state: RootState) {
    return state.ui.mode
}

export function get_filters(state: RootState) {
    return state.ui.filters
}

export function get_filter_value(state: RootState, attr_name: string) {
    return state.ui.filters[attr_name]
}


export const get_is_loading = createSelector(
    (state: RootState) => state.ui._loading, // dependency
    (loading_state) => {
        return Object.values(loading_state).some(v => v == true)
    }
)


export function get_tooltip(state: RootState) {
    return state.ui.tooltip
}


/* add a prefix to the input, to aid with sorting */
function _sort_spell_type_sort_key(spell_type: string) {

    let prefix = "50" // start middle
    if (spell_type == "raid")           { prefix = "60"} // raid cd's after class
    if (spell_type.startsWith("other")) { prefix = "80"} // other types go behind

    return [prefix, spell_type].join("-")
}

/* Sort spell types as:
   - boss
   - specs
   - other
*/
export function sort_spell_types(spell_types: string[]) {
    return spell_types.sort((a, b) => {
        const key_a = _sort_spell_type_sort_key(a)
        const key_b = _sort_spell_type_sort_key(b)
        return key_a > key_b ? 1 : -1
    })
}


////////////////////////////////////////////////////////////////////////////////
// Slice
//
interface UiSliceStateFilterKilltime {
    min: number | undefined
    max: number | undefined
}


interface UiSliceStateFilters {

    // player filters
    role: { [key: string]: boolean },
    class: { [key: string]: boolean },
    spec: { [key: string]: boolean },
    covenant: { [key: string]: boolean },

    // fight filters
    killtime: UiSliceStateFilterKilltime
}

interface UiSliceStateTooltipPosition {
    x: number
    y: number
}

interface UiSliceStateTooltip {
    content: string
    position: UiSliceStateTooltipPosition

}


interface UiSliceState {

    mode: "none" | "spec_ranking" | "comp_ranking"

    /** elements that are loading */
    _loading: { [key: string]: boolean }

    /** currently selected spec */
    spec_slug: string

    /** currently selected boss */
    boss_slug: string

    // Timeline Options
    settings: { [key: string]: boolean}

    // fight/player filter settings
    filters: { [key: string]: { [key: string]: boolean | null } }

    tooltip: UiSliceStateTooltip
}


const INITIAL_STATE: UiSliceState = {

    mode: "none",

    _loading: {}, // elements that are loading

    spec_slug: "", // currently selected spec
    boss_slug: "", // currently selected boss

    // Timeline Options
    settings: {
        show_casticon: true,
        show_casttime: true,
        show_duration: true,
        show_cooldown: true,
    },

    // fight/player filter settings
    filters: {

        // player filters
        role: {},
        class: { boss: false },  // for now, bosses are hidden by default (except the pinned ones)
        spec: {},
        covenant: {},

        // fight filters
        killtime: {min: null, max: null},
    },

    tooltip: {
        content: "",
        position: {x: 0, y: 0}
    }
}


const SLICE = createSlice({
    name: "ui",

    initialState: INITIAL_STATE,

    reducers: {

        set_boss_slug: (state, action: PayloadAction<string>) => {
            state.boss_slug = action.payload
            return state
        },

        set_spec_slug: (state, action: PayloadAction<string>) => {
            state.spec_slug = action.payload
            return state
        },

        update_settings: (state, action) => {
            state.settings = {...state.settings, ...action.payload}
            return state
        },

        // Filters
        set_filter: (state, action) => {
            const { group, name, value } = action.payload
            state.filters[group] = state.filters[group] || {}
            state.filters[group][name] = value
            // state.filters = {...state.filters, ...action.payload}
            return state
        },

        set_filters: (state, action) => {
            state.filters = {...state.filters, ...action.payload}
            return state
        },

        // loading
        set_loading: (state, action: PayloadAction<{key: string, value: boolean}>) => {
            state._loading[action.payload.key] = action.payload.value
            return state
        },

        set_mode: (state, action) => {
            state.mode = action.payload
            return state
        },

        set_tooltip: (state, action) => {
            const {content, position } = action.payload
            state.tooltip.content = content
            state.tooltip.position = position
            return state
        }
    },
})


export const {
    set_boss_slug,
    set_filter,
    set_filters,
    set_mode,
    set_spec_slug,
    set_tooltip,
    update_settings,
} = SLICE.actions


export default SLICE.reducer
