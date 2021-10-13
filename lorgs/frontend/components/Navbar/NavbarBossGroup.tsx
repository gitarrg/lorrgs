import { useSelector } from 'react-redux';

import NavbarBossButton from "./NavbarBossButton";
import NavbarGroup from './NavbarGroup';
import { get_bosses } from '../../store/bosses';


////////////////////////////////////////////////////////////////////////////////
export default function NavbarBossGroup() {
    const bosses = useSelector(state => get_bosses(state));

    return (
        <NavbarGroup className="navbar_boss">
            {Object.values(bosses).map(boss =>
                <NavbarBossButton key={boss.full_name_slug} boss={boss} />
            )}
        </NavbarGroup>
    );
}
